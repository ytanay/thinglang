from thinglang.execution.errors import ReturnInConstructorError, EmptyMethodBody, EmptyThingDefinition, \
    ArgumentCountMismatch, UnresolvedReference
from thinglang.execution.resolver import Resolver
from thinglang.execution.stack import Frame
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.errors import ParseErrors
from thinglang.parser.symbols import BaseSymbol
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import MethodDefinition, ThingDefinition
from thinglang.parser.symbols.functions import ReturnStatement, MethodCall, Access
from thinglang.utils.collection_utils import flatten_list, flatten_recursively, emit_recursively


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

def inspects(*args):
    def decorator(func):
        func.inspected_types = args
        return func
    return decorator


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

        assert node.parent is parent, 'expected node {} to have parent {} but got {}'.format(node, parent, node.parent)

        if node.implements(ThingDefinition):
            self.scoping.instance = node

        self.inspect(node)

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


    def inspect(self, node):
        for inspection in Analysis.INSPECTIONS:
            if isinstance(node, inspection.inspected_types):
                self.errors.extend(inspection(node))

    def report_exception(self, error):
        self.errors.append(error)

    @classmethod
    @inspects(ThingDefinition)
    def verify_thing_definitions(cls, node):
        if not node.children:
            yield EmptyThingDefinition()

    @classmethod
    @inspects(MethodDefinition)
    def verify_method_definitions(cls, node):
        if not node.children:
            yield EmptyMethodBody()

        if node.is_constructor() and list(node.find(lambda x: isinstance(x, ReturnStatement))):
            raise ReturnInConstructorError(node)


Analysis.INSPECTIONS = [getattr(Analysis, member) for member in dir(Analysis) if hasattr(getattr(Analysis, member), 'inspected_types')]


def analyze(ast):

    analysis = Analysis(ast).run()
    if analysis.errors:
        raise ParseErrors(*analysis.errors) if len(analysis.errors) > 1 else analysis.errors[0]
