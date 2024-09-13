import datetime
import errno
import multiprocessing
import queue
import socket
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Union
import requests
from psplpy.other_utils import is_sys
from psplpy.serialization_utils import Serializer


def _find(func: Callable, try_ports: list[int] = None, exclude_ports: list[int] = None,
          try_range: tuple[int, int] = None) -> int | None:
    ports = (try_ports or []) + list(range(*try_range))
    exclude_ports = exclude_ports or []
    for port in ports:
        if port not in exclude_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    result = func(s, port)
                    if result is not None:
                        return result
            except socket.error:
                continue


def find_running_port(host: str = '127.0.0.1', try_ports: list[int] = None, exclude_ports: list[int] = None,
                      try_range: tuple[int, int] = None, timeout: float = 0.5) -> int | None:
    def _test(s: socket.socket, port: int):
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        if result == 0:
            return port

    return _find(_test, try_ports, exclude_ports, try_range)


def find_free_port(host: str = '127.0.0.1', try_ports: list[int] = None, exclude_ports: list[int] = None,
                   try_range: tuple[int, int] = (1024, 65536)) -> int | None:
    def _test(s: socket.socket, port: int):
        s.bind((host, port))
        return port

    return _find(_test, try_ports, exclude_ports, try_range)


class ClientSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, client_socket: socket.socket = None,
                 client_host: str = None, client_port: int = 12345):
        self.host = host
        self.port = port
        self._serializer = Serializer()
        self.client_host = client_host
        self.client_port = client_port
        self.client_socket = client_socket

        self._length_bytes = 5

        if self.client_socket:
            if is_sys(is_sys.WINDOWS):
                self.client_socket.setblocking(True)
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)

    def connect(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024 * 1024)
        # use the certain address of the client to connect the server
        if self.client_host and self.client_port:
            self.client_socket.bind((self.client_host, self.client_port))
        self.client_socket.connect((self.host, self.port))

    def _get_length(self, data: bytes) -> bytes:
        # for 5 bytes unsigned int, the max data length is 2**40 - 1, namely about 1tb
        bytes_result = len(data).to_bytes(self._length_bytes, byteorder='big')
        return bytes_result

    def _recv_length(self) -> int:
        byte_result = self.client_socket.recv(self._length_bytes)
        return int.from_bytes(byte_result, byteorder='big')

    def send(self, data: bytes):
        return self.client_socket.sendall(self._get_length(data) + data)

    def recv(self) -> bytes:
        length = self._recv_length()
        data = bytearray()
        while len(data) < length:
            new_data = self.client_socket.recv(length - len(data))
            data += new_data
            if len(new_data) == 0:  # avoid the sender ended by accident, lead to get into the infinite loop
                return bytes(data)
        return bytes(data)

    def recvf(self, output_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(output_path, 'wb') as f:
            while True:
                data = self.client_socket.recv(bufsize)
                if not data:
                    break
                f.write(data)

    def sendf(self, input_path: str | Path, bufsize: int = 1024 * 1024 * 16) -> None:
        with open(input_path, 'rb') as f:
            while True:
                data = f.read(bufsize)
                if not data:
                    break
                self.client_socket.send(data)

    def send_pickle(self, data: Any) -> None:
        return self.send(self._serializer.dump_pickle(data))

    def recv_pickle(self) -> Any | None:
        if data := self.recv():
            return self._serializer.load_pickle(data)

    def close(self) -> None:
        return self.client_socket.close()


class ServerSocket:
    def __init__(self, host: str = '127.0.0.1', port: int = 12345, backlog: int = 64):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(backlog)
        self.server_socket.setblocking(False)

    def accept(self) -> tuple[ClientSocket, Any] | tuple[None, None]:
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                return ClientSocket(client_socket=client_socket), addr
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN:
                    time.sleep(0.01)
                    continue
                elif e.errno == errno.EBADF:
                    return None, None
                elif is_sys(is_sys.WINDOWS):
                    if e.errno == errno.WSAENOTSOCK:
                        return None, None
                raise e

    def handle(self, handler: Callable, *args, **kwargs) -> None:
        def _handle():
            while True:
                client_socket, addr = self.accept()
                if not (client_socket and addr):
                    break
                handle_thread = threading.Thread(target=handler, args=(client_socket, addr, *args), kwargs=kwargs)
                handle_thread.daemon = True
                handle_thread.start()

        threading.Thread(target=_handle).start()

    def close(self) -> None:
        self.server_socket.close()


class MpHttpError(Exception):
    def __init__(self, *args, traceback_info: str = ''):
        super().__init__(*args)
        self.traceback_info = traceback_info

    def __str__(self):
        return self.traceback_info
    __repr__ = __str__


class MpHttpServer:
    SUBMIT = '/submit'
    FETCH = '/fetch'
    GET_LOAD = '/get_load'
    GET_PROGRESS = '/get_progress'
    _POLL_INTERVAL = 0.1

    def __init__(self, host: str = '0.0.0.0', port: int = 80, workers: int = 1, show_info: bool = True,
                 max_fetch_timeout: float = 3600, result_timeout: float = 3600):
        self.host, self.port, self.workers, self.show_info = host, port, workers, show_info
        self.max_fetch_timeout, self.result_timeout = max_fetch_timeout, result_timeout
        self._task_id = 0
        self._lock = multiprocessing.Lock()  # Do not use threading.Lock, can't be pickled on Windows
        self._s = Serializer()
        self._result_dict: dict[int, MpHttpServer._TaskResult] = {}
        self._req_que = multiprocessing.Queue()
        self._result_que = multiprocessing.Queue()
        self._closed_flag = multiprocessing.Value('b', False)
        self._load = multiprocessing.Value('i', 0)

    class _SubTask:
        def __init__(self, task_id: int, sub_task_id: int, data: Any):
            self.task_id = task_id
            self.sub_task_id = sub_task_id
            self.data = data
            self.result = None

    class _TaskResult:
        def __init__(self, task_num: int):
            self.task_num = task_num
            self.finished_task_num = 0
            self.finished_task_list = [None] * task_num  # [None] * 0 = []
            self.is_finished = threading.Event()
            self.finished_time = None
            if self.task_num == 0:
                self._set_finished()

        def _set_finished(self):
            self.is_finished.set()
            self.finished_time = time.time()

        def add_finished_subtask(self, sub_task: 'MpHttpServer._SubTask') -> None:
            self.finished_task_list[sub_task.sub_task_id] = sub_task.result
            self.finished_task_num += 1
            if self.finished_task_num == self.task_num:
                self._set_finished()

    class _RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, s: 'MpHttpServer', *args, **kwargs):
            self.s = s
            super().__init__(*args, **kwargs)

        def log_request(self, code="-", size="-"):
            pass

        def log_message(self, format, *args):
            if self.s.show_info:
                super().log_message(format, *args)

        def _put_data(self, data: Any) -> int:
            sub_task_id = 0
            with self.s._lock:
                task_id = self.s._task_id
                self.s._task_id += 1
            for sub_data in data:
                self.s._req_que.put(self.s._SubTask(task_id, sub_task_id, sub_data))
                sub_task_id += 1
            self.s._result_dict[task_id] = self.s._TaskResult(len(data))
            return task_id

        def _fetch_result(self, task_id: int, timeout: float) -> list[Any] | TimeoutError | KeyError:
            timeout = timeout if timeout <= self.s.max_fetch_timeout else self.s.max_fetch_timeout
            if self.s._result_dict.get(task_id):
                if self.s._result_dict[task_id].is_finished.wait(timeout):
                    return self.s._result_dict.pop(task_id).finished_task_list
                return TimeoutError(f'Fetch task {task_id} result timeout after {timeout}s')
            return KeyError(f'Task {task_id} result not exist or expired')

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            data = []
            if content_length:
                post_data = self.rfile.read(content_length)
                data = self.s._s.load_pickle(post_data)

            code = 200
            if self.path == MpHttpServer.GET_LOAD:
                result = self.s._load.value / self.s.workers
            elif self.path == MpHttpServer.GET_PROGRESS:
                task = self.s._result_dict.get(data)
                result = (0, 0)
                if task:
                    result = (task.finished_task_num, task.task_num)
            elif self.path == MpHttpServer.SUBMIT:
                result = self._put_data(data)
            elif self.path == MpHttpServer.FETCH:
                result = self._fetch_result(**data)
            else:
                code, result = 404, None

            response = self.s._s.dump_pickle(result)
            self.log_message('"%s" %s %s %s', self.requestline, str(code),
                             str(len(response)), str(self.client_address))
            self.send_response(code)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    @staticmethod
    def _get_subtask(func: Callable):
        def wrapper(self, que: multiprocessing.Queue, *args, **kwargs) -> None:
            while True:
                try:
                    sub_task: MpHttpServer._SubTask = que.get(timeout=MpHttpServer._POLL_INTERVAL)
                except queue.Empty:
                    if self._closed_flag.value:
                        break
                    continue
                func(self, sub_task, *args, **kwargs)
        return wrapper

    @_get_subtask
    def _result_distribution(self, sub_task: Union[multiprocessing.Queue, 'MpHttpServer._SubTask']) -> None:
        self._result_dict[sub_task.task_id].add_finished_subtask(sub_task)

    def _cleanup_expired_results(self):
        last_cleanup_time = time.time()
        while True:
            if self._closed_flag.value:
                break
            if time.time() - last_cleanup_time > self.result_timeout / 10:
                expired_task_ids = []
                for task_id, task in self._result_dict.items():
                    if task.is_finished.is_set() and time.time() - task.finished_time > self.result_timeout:
                        expired_task_ids.append(task_id)
                for task_id in expired_task_ids:
                    self._result_dict.pop(task_id)
                    if self.show_info:
                        time_str = datetime.datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
                        sys.stderr.write(f'Warning - {time_str} - Result of task {task_id} has expired\n')
                last_cleanup_time = time.time()
            else:
                time.sleep(self._POLL_INTERVAL)

    def init(self) -> None: ...

    def main_loop(self, data: Any) -> Any:
        return data

    def _main_process(self, req_que: multiprocessing.Queue, result_que: multiprocessing.Queue) -> None:
        @MpHttpServer._get_subtask
        def _process(self, sub_task: Union[multiprocessing.Queue, 'MpHttpServer._SubTask']) -> None:
            with self._load.get_lock():
                self._load.value += 1
            try:
                result = self.main_loop(sub_task.data)
                sub_task.result = result
            except Exception:
                sub_task.result = MpHttpError(traceback_info=traceback.format_exc())
            finally:
                del sub_task.data
                result_que.put(sub_task)
                with self._load.get_lock():
                    self._load.value -= 1

        self.init()
        _process(self, req_que)

    def run_server(self, new_thread: bool = False) -> 'MpHttpServer':
        threading.Thread(target=self._result_distribution, args=(self._result_que,)).start()
        threading.Thread(target=self._cleanup_expired_results).start()
        for _ in range(self.workers):
            multiprocessing.Process(target=self._main_process, args=(self._req_que, self._result_que)).start()
        self._httpd = ThreadingHTTPServer((self.host, self.port),
                                          lambda *args, **kwargs: self._RequestHandler(self, *args, **kwargs))
        if self.show_info:
            sys.stderr.write(f"Starting server on ({self.host}, {self.port})...\n")
        if new_thread:
            threading.Thread(target=self._httpd.serve_forever, kwargs={'poll_interval': self._POLL_INTERVAL}).start()
        else:
            self._httpd.serve_forever(poll_interval=self._POLL_INTERVAL)
        return self

    def close_server(self) -> None:
        self._closed_flag.value = True
        self._httpd.shutdown()
        self._httpd.server_close()


class MpHttpClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 80, server: MpHttpServer = None):
        self.host, self.port = host, port
        if server:
            self.host, self.port = server.host if server.host != '0.0.0.0' else '127.0.0.1', server.port
        self._s = Serializer()

    def _req(self, data: Any, path: str) -> Any:
        pickled_data = self._s.dump_pickle(data)
        resp = requests.post(f'http://{self.host}:{self.port}{path}', data=pickled_data)
        return self._s.load_pickle(resp.content)

    def submit(self, data_list: list | tuple) -> int:
        """Getting the task_id for fetching data from the server"""
        return self._req(data_list, MpHttpServer.SUBMIT)

    def fetch(self, task_id: int, timeout: float = 3600) -> list[Any]:
        """The max timeout time depends on the setting of the server"""
        result = self._req({'task_id': task_id, 'timeout': timeout}, MpHttpServer.FETCH)
        if isinstance(result, (TimeoutError, KeyError)):
            raise result
        return result

    def batch(self, data_list: list | tuple, timeout: float = 3600) -> list[Any]:
        return self.fetch(self.submit(data_list), timeout)

    def get(self, data: Any, timeout: float = 3600) -> Any:
        return self.batch([data], timeout)[0]

    def get_load(self) -> float:
        return self._req(None, MpHttpServer.GET_LOAD)

    def get_progress(self, task_id: int) -> tuple[int, int]:
        """return the tuple (finished_task_num, total_task_num)"""
        return self._req(task_id, MpHttpServer.GET_PROGRESS)
