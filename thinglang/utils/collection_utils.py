import functools
import types


def drain(func):
    """
    Drains a generator function into a list
    """
    @functools.wraps(func)
    def inner(*args, **kwargs) -> list:
        return list(func(*args, **kwargs))

    return inner


def subclasses(cls):
    for subclass in cls.__subclasses__():
        yield from subclasses(subclass)
        yield subclass


def predicated(func):
    def wrapped(self, cls=object, predicate=lambda x: True, **kwargs):
        if isinstance(cls, types.FunctionType):
            return func(self, cls, **kwargs)

        assert cls is not object or not predicate(None), 'Must provide CLS or predicate'

        def predicate_func(node):
            return isinstance(node, cls) and predicate(node)

        return func(self, predicate_func, **kwargs)

    return wrapped


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
