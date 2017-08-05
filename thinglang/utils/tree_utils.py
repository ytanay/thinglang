import types

from thinglang.parser.nodes.classes import ThingDefinition, MethodDefinition


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
        self.inspections = sorted((getattr(self, member) for member in dir(self) if
                            hasattr(getattr(self, member), 'predicate')), key=lambda x: x.priority)

        self.current_thing, self.current_method = None, None

    def run(self):
        self.traverse(self.ast)

    def traverse(self, node):
        self.inspect(node)

        for child in node.children:
            self.traverse(child)

    def inspect(self, node):
        for inspection in self.inspections:
            if inspection.predicate(node):
                inspection(node)

    @inspects(ThingDefinition)
    def update_thing_context(self, node: ThingDefinition):
        self.current_thing = node

    @inspects(MethodDefinition)
    def update_method_context(self, node: MethodDefinition):
        self.current_method = node
