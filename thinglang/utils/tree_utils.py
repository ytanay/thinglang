import types

from thinglang.utils.stack import Frame


def predicated(func):
    def wrapped(self, cls=object, predicate=lambda x: True, **kwargs):
        if isinstance(cls, types.FunctionType):
            return func(self, cls, **kwargs)

        assert cls is not object or not predicate(None), 'Must provide CLS or predicate'

        def predicate_func(node):
            return isinstance(node, cls) and predicate(node)

        return func(self, predicate_func, **kwargs)

    return wrapped


def inspects(*args, predicate=None, priority=0):
    if predicate is None:
        def predicate(node):
            return isinstance(node, args) if args else True

    def decorator(func):
        func.predicate = predicate
        func.priority = priority
        return func
    return decorator


class TreeTraversal(object):

    def __init__(self, ast):
        self.ast = ast
        self.results = []
        self.scoping = Frame(expected_key_type=object)
        self.inspections = sorted((getattr(self, member) for member in dir(self) if
                            hasattr(getattr(self, member), 'predicate')), key=lambda x: x.priority)

    def run(self):
        self.traverse(self.ast)

    def traverse(self, node, parent=None):
        self.inspect(node, parent)

        if node.SCOPING:
            self.scoping.enter()

        for child in node.children:
            self.traverse(child, node)

        if node.SCOPING:
            self.scoping.exit()

    def inspect(self, node, parent):
        for inspection in self.inspections:
            if inspection.predicate(node):
                result = inspection(node)
                if isinstance(result, types.GeneratorType):
                    self.results.extend(result)
