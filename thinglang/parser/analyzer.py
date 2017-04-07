from thinglang.execution.errors import ReturnInConstructorError, EmptyMethodBody, EmptyThingDefinition, \
    ArgumentCountMismatch
from thinglang.parser.symbols.classes import MethodDefinition, ThingDefinition
from thinglang.parser.symbols.functions import ReturnStatement, MethodCall


def verify_method_definitions(ast):
    for child in ast.find(lambda x: isinstance(x, MethodDefinition)):
        if child.is_constructor() and list(child.find(lambda x: isinstance(x, ReturnStatement))):
            raise ReturnInConstructorError(child)

        if not child.children:
            raise EmptyMethodBody()


def verify_thing_definitions(ast):
    for child in ast.find(lambda x: isinstance(x, ThingDefinition)):
        if not child.children:
            raise EmptyThingDefinition()


def analyze_method_resolution(ast):
    for child in ast.find(MethodCall):
        if child.target[0].is_self():
            thing_definition = child.upwards(ThingDefinition)
        else:
            thing_definition = ast.find(ThingDefinition, lambda x: x.name == child.target[0], single=True)

        if thing_definition is None:
            print('Warning: method resolution cannot be validated!')
        elif len(child.arguments) != len(thing_definition.find(MethodDefinition, lambda x: x.name == child.target[1], single=True).arguments):
            raise ArgumentCountMismatch()


def validate_tree_hierarchy(node, parent=None):
    assert node.parent is parent, 'expected node {} to have parent {} but got {}'.format(node, parent, node.parent)

    for child in node.children:
        validate_tree_hierarchy(child, node)
class Analysis(object):
    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.scoping = Frame(expected_key_type=object)
        heap = {LexicalIdentifier("Output"): {LexicalIdentifier("write"): {}}}
        heap.update({
            x.name: x for x in self.ast.children
        })
        self.resolver = Resolver(self.scoping, heap)

    def run(self):
        self.traverse()
        return self

    def traverse(self, node=None, parent=None):
        node = node or self.ast

        if node.implements(AssignmentOperation):
            self.scoping[node.name] = True

        if node.references():
            for ref in (x for x in emit_recursively(node.references(), (Access, LexicalIdentifier)) if not self.validate_scoping(x)):
                self.report_exception(UnresolvedReference(ref))

        if node.SCOPING:
            self.scoping.enter()

        for child in node.children:
            self.traverse(child, node)

        if node.SCOPING:
            self.scoping.exit()

    def validate_scoping(self, reference):
        return self.resolver.lookup(reference) is not Resolver.UNRESOLVED_REFERENCE

def analyze(ast):
    validate_tree_hierarchy(ast)
    analyze_method_resolution(ast)
    verify_method_definitions(ast)
    verify_thing_definitions(ast)
