import collections

import functools
import types


def flatten_list(l):
    """
    Flatten a 2-level deep list
    """
    return [item for sublist in l for item in sublist]


def emit_recursively(iterable, expected_type):
    """
    Recursively descend into an arbitrarily nested collection, emitting values that are an instance of expected_type
    """
    targets = collections.deque([iterable])
    while targets:
        target = targets.popleft()
        if isinstance(target, expected_type):
            yield target
            continue
        try:
            targets.extend(target)
        except TypeError:
            pass


def combine(*args) -> dict:
    """
    Combines multiple dictionaries into one, where later argument override earlier ones.
    Mutates the first argument.
    :return: combined dict
    """
    value = args[0]

    for arg in args[1:]:
        value.update(arg)

    return value


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
