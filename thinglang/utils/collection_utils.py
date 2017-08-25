import functools

def drain(func):
    """
    Drains a generator function into a list
    """
    @functools.wraps(func)
    def inner(*args, **kwargs) -> list:
        return list(func(*args, **kwargs))

    return inner


def subclasses(cls):
    """
    Recursively emit subclasses of cls
    """
    for subclass in cls.__subclasses__():
        yield from subclasses(subclass)
        yield subclass


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
