import time


class TimeRecorder:
    def __init__(self, name):
        # print(name + u" start")
        self.name = name
        self.startTime = time.time()

    def __del__(self):
        print("{0} end, time used: {1} s".format(self.name, time.time() - self.startTime))


def log_time_with_name(name=None):
    def wrapper(func):
        def wrapper2(*args, **kwargs):
            _name = name
            if name is None:
                _name = func.func_name
            else:
                _name = name
            # print(_name + u" start")
            startTime = time.time()
            res = func(*args, **kwargs)
            print("{0} end, time used: {1} s".format(_name, time.time() - startTime))
            return res

        return wrapper2

    return wrapper


def log_time(func):
    def wrapper(*args, **kwargs):
        # print(func.func_name + u" start")
        startTime = time.time()
        ret = func(*args, **kwargs)
        print("{0} end, time used: {1} s".format(func.func_name, time.time() - startTime))
        return ret

    return wrapper
