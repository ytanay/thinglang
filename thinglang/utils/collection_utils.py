import collections

import functools


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
