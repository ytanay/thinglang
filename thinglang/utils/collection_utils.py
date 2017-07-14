import collections


def flatten_list(l):
    return [item for sublist in l for item in sublist]


def emit_recursively(iterable, expected_type):
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


def combine(*args):
    value = args[0]
    for arg in args[1:]:
        value.update(arg)
    return value


def drain(func):
    """
    Drains a generator function
    """
    def inner(*args, **kwargs):
        return list(func(*args, **kwargs))

    return inner