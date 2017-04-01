import types


def predicated(func):
    def wrapped(self, cls=object, predicate=lambda x: True, **kwargs):
        if isinstance(cls, types.FunctionType):
            return func(self, cls, **kwargs)

        assert cls is not object or not predicate(None), 'Must provide CLS or predicate'

        predicate_func = lambda node: (isinstance(node, cls) and predicate(node))
        return func(self, predicate_func, **kwargs)

    return wrapped
