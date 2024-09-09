import time
from threading import Thread
from tests.__init__ import *
from psplpy.other_utils import *


def test_is_sys():
    assert is_sys(is_sys.LINUX) is True
    assert is_sys(is_sys.WINDOWS) is False


def test_recursive_convert():
    data = [1, (2, [3, 4])]
    assert recursive_convert(data, to=list) == [1, [2, [3, 4]]]
    assert recursive_convert(data, to=tuple) == (1, (2, (3, 4)))


def test_split_list():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert split_list(lst, 4) == [[1, 2, 3], [4, 5], [6, 7], [8, 9]]


def test_get_key_from_value():
    dct = {'a': 1, 'b': 2, 'c': 1, 'd': 1}
    assert get_key_from_value(dct, 1) == 'a'
    assert get_key_from_value(dct, 2, find_all=True) == ['b']
    assert get_key_from_value(dct, 1, find_all=True) == ['a', 'c', 'd']
    assert get_key_from_value(dct, 3, allow_null=True) is None
    assert get_key_from_value(dct, 3, find_all=True, allow_null=True) is None
    try:
        get_key_from_value(dct, 3)
    except KeyError as e:
        print(e)
    else:
        assert False


def test_get_env():
    assert get_env('SERVICE') == 'psplpy'
    try:
        get_env('S')
    except KeyError as e:
        pass
    else:
        raise AssertionError


def test_perf_counter():
    p = PerfCounter()
    time.sleep(0.1)
    assert int(p.elapsed()) == int(0.1 * 1000)
    time.sleep(0.2)
    p.show('perf')


def test_timeout_checker():
    def checker(timeout: float, unique_id: Any = None, check_time: float = None,
                func: str = 'ret_false', end_loop_time: float = 10000):
        t_start = time.time()
        while getattr(TimeoutChecker(timeout, unique_id=unique_id), func)():
            if time.time() - t_start > end_loop_time:
                break
            time.sleep(0.01)
        print(time.time() - t_start)
        assert int(time.time() - t_start) == check_time or timeout

    Thread(target=checker, kwargs={'timeout': 1, 'unique_id': 1}).start()
    timeout = 2
    Thread(target=checker, kwargs={'timeout': 2, 'unique_id': 2}).start()
    time.sleep(timeout + 0.5)

    kwargs = {'timeout': 2, 'unique_id': 1, 'check_time': 1, 'func': 'raise_err', 'end_loop_time': 1}
    Thread(target=checker, kwargs=kwargs).start()
    try:
        checker(timeout=1, unique_id=2, func='raise_err')
    except Exception as e:
        assert isinstance(e, TimeoutError)


def test_screenshot_maker():
    pass
    # ScreenShotMaker()


def tests():
    print('test other utils')
    test_is_sys()
    test_recursive_convert()
    test_split_list()
    test_get_key_from_value()
    test_get_env()
    test_timeout_checker()
    test_screenshot_maker()
    test_perf_counter()


if __name__ == '__main__':
    tests()
