from concurrent import futures

from tests.__init__ import *
from psplpy.network_utils import *


def get_ip_address():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("114.114.114.114", 80))  # connect to a public ip address
        ip_address = temp_socket.getsockname()[0]  # get the host's ip
        temp_socket.close()
        return ip_address
    except socket.error:
        return None


port = 12345
host_ip = get_ip_address()
client_port = find_free_port(host_ip, try_range=(12345, 12999))
data = b"Hello World" * 1024 * 32


def sender():
    def handler(client_socket: ClientSocket, addr):
        print(f'client {addr}')
        assert addr == (host_ip, client_port)

        received_data = client_socket.recv()
        assert received_data == data
        client_socket.send(data)
        recv_tmp_file = tmp_dir / 'recv_tmp.tmp'
        client_socket.recvf(recv_tmp_file)
        assert tmp_file.read_text() == recv_tmp_file.read_text()

        tmp_file.unlink()
        recv_tmp_file.unlink()
        client_socket.close()
        server.close()

    server = ServerSocket(port=port)
    server.handle(handler)


def recver():
    client = ClientSocket(port=port, client_host=host_ip, client_port=client_port)
    client.connect()
    client.send(data)
    received_data = client.recv()
    assert received_data == data
    tmp_file.write_bytes(data)
    client.sendf(tmp_file)
    client.close()


def test_find():
    def handler(client_socket: ClientSocket, addr):
        client_socket.close()

    test_port = find_free_port(host_ip, [12345, ], [12346, ], (12345, 12999))
    print(f'test port {test_port}')
    s = ServerSocket(host=host_ip, port=test_port)
    s.handle(handler)
    assert find_running_port(host=host_ip, try_range=(test_port - 100, test_port + 100)) == test_port
    assert find_running_port(host=host_ip, try_ports=[test_port, ], exclude_ports=[test_port, ],
                             try_range=(test_port - 100, test_port + 100)) is None

    s.close()


def test_mp_http():
    class TestServer(MpHttpServer):
        def init(self) -> None:
            self.num = 1

        def main_loop(self, data: Any) -> Any:
            time.sleep(data / 1)
            return {'result': data, 'num': self.num}

    def show_load(c: MpHttpClient):
        time.sleep(0.25)
        return c.get_load()

    s = TestServer(port=find_free_port(), workers=6, max_fetch_timeout=2, result_timeout=1).run_server(new_thread=True)
    time.sleep(0.25)
    c = MpHttpClient(server=s)

    # test get_load and batch
    load_results = futures.ThreadPoolExecutor().map(show_load, [c])  # starting a new thread to get the load
    result = c.batch([0.5, 0.75, 1])
    load_results = list(load_results)
    assert load_results == [0.5], load_results
    assert result == [{'result': 0.5, 'num': 1}, {'result': 0.75, 'num': 1}, {'result': 1, 'num': 1}], result

    # test get_progress
    data_list = [0.5, 0.75, 1]
    task_id = c.submit(data_list)
    assert isinstance(task_id, int)
    task_progress = c.get_progress(task_id)
    assert task_progress == (0, len(data_list)), task_progress
    time.sleep(0.75 + 0.05)
    task_progress = c.get_progress(task_id)
    assert task_progress == (2, len(data_list)), task_progress
    time.sleep(1 - 0.75)

    # test task result expiration and task fetch timeout
    time.sleep(2)
    try:
        result = c.fetch(task_id)
    except KeyError as e:
        print(e)
    else:
        assert False
    task_id = c.submit([3])
    try:
        result = c.fetch(task_id)
    except TimeoutError as e:
        print(e)
    else:
        assert False
    time.sleep(1.5)

    # test no load
    assert c.get_load() == 0
    time.sleep(0.25)

    # test send empty list
    task_id = c.submit([])
    assert c.fetch(task_id) == []
    s.close_server()


def tests():
    with futures.ThreadPoolExecutor() as executor:
        sender_future = executor.submit(sender)
        time.sleep(0.1)
        recver_future = executor.submit(recver)
        time.sleep(0.1)
        sender_future.result(), recver_future.result()
    test_find()
    test_mp_http()


if __name__ == '__main__':
    tests()
