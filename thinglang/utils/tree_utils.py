from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.definitions.thing_definition import ThingDefinition


def inspects(*args, predicate=None, priority=0):
    """
    Tags a TreeTraversal inspector method
    :param args: AST node types accepted by this inspector, if predicate is not set
    :param predicate: a custom entrance function - overrides args
    :param priority: the order in which this inspector will be called, relative to other inspectors
    """
    if predicate is None:
        def predicate(node):
            return isinstance(node, args) if args else True

    def decorator(func):
        func.predicate = predicate
        func.priority = priority
        return func

    return decorator


class TreeTraversal(object):
    """
    A helper class implementing DFS passes over the AST.
    Automatically keeps track of the current ThingDefinition and MethodDefinition being analyzed
    """

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
