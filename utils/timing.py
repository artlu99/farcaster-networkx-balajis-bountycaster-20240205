from time import time


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        end = time()-t1
        return result, end
    return wrapper
