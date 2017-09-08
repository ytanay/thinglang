import functools


def drain(predicate=lambda x: True):
    """
    Drains a generator function into a list
    """

    def wrapper(func):

        @functools.wraps(func)
        def inner(*args, **kwargs) -> list:
            return [x for x in func(*args, **kwargs) if predicate(x)]

        return inner

    return wrapper


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
