import functools
from typing import Iterable, Type, Sequence


def drain(predicate=lambda x: True):
    """
    Drains a generator function into a list, optionally filtering using predicate
    """
    def wrapper(func):

        @functools.wraps(func)
        def inner(*args, **kwargs) -> list:
            return [x for x in func(*args, **kwargs) if predicate(x)]

        return inner

    return wrapper


def subclasses(cls: Type) -> Iterable[type]:
    """
    Recursively emit subclasses of cls
    """
    for subclass in cls.__subclasses__():
        yield from subclasses(subclass)
        yield subclass


def chunks(collection: Sequence, n: int) -> Iterable[list]:
    """
    Yield successive n-sized chunks from collection.
    """
    for i in range(0, len(collection), n):
        yield collection[i:i + n]


@drain()
def flatten(lst: Iterable) -> list:
    """
    Recursively descend into lst, producing a flattened list from its contents.
    """
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
