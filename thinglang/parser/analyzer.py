import types

from thinglang.execution.builtins import BUILTINS, INTERNAL_MEMBER
from thinglang.execution.errors import ReturnInConstructorError, EmptyMethodBody, EmptyThingDefinition, \
    ArgumentCountMismatch, UnresolvedReference
from thinglang.execution.resolver import Resolver
from thinglang.execution.stack import Frame
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.errors import ParseErrors
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import MethodDefinition, ThingDefinition
from thinglang.parser.symbols.functions import ReturnStatement, MethodCall, Access
from thinglang.utils.collection_utils import emit_recursively
from thinglang.utils.union_types import ACCESS_TYPES


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
        heap = {
            LexicalIdentifier(x.INTERNAL_NAME): x.EXPORTS for x in BUILTINS
        }
        heap.update({
            x.name: x for x in self.ast.children
        })
        self.resolver = Resolver(self.scoping, heap)

        self.inspections = [getattr(self, member) for member in dir(self) if hasattr(getattr(self, member), 'inspected_types')]

    def run(self):
        self.traverse()
        return self

    def traverse(self, node=None, parent=None):
        node = node or self.ast

        assert node.parent is parent, 'expected node {} to have parent {} but got {}'.format(node, parent, node.parent)

        self.inspect(node)

        if node.SCOPING:
            self.scoping.enter()

        for child in node.children:
            self.traverse(child, node)

        if node.SCOPING:
            self.scoping.exit()

    def validate_scoping(self, reference):
        return self.resolver.lookup(reference) is not Resolver.UNRESOLVED_REFERENCE

    def inspect(self, node):
        for inspection in self.inspections:
            if not inspection.inspected_types or isinstance(node, inspection.inspected_types):
                result = inspection(node)
                if isinstance(result, types.GeneratorType):
                    self.errors.extend(result)

    def report_exception(self, error):
        self.errors.append(error)

    @inspects()
    def verify_reference_dependencies(self, node):
        if node.references():
            for ref in (x for x in emit_recursively(node.references(), (Access, LexicalIdentifier)) if not self.validate_scoping(x)):
                yield UnresolvedReference(ref)

    @inspects(AssignmentOperation)
    def mark_variable_deceleration(self, node):
        self.scoping[node.name] = True


    @inspects(ThingDefinition)
    def verify_thing_definitions(self, node):
        self.scoping.instance = node

        if not node.children:
            yield EmptyThingDefinition()

    @inspects(MethodDefinition)
    def verify_method_definitions(self, node):
        if not node.children:
            yield EmptyMethodBody()

        if node.is_constructor() and list(node.find(lambda x: isinstance(x, ReturnStatement))):
            raise ReturnInConstructorError(node)


def analyze(ast):

    analysis = Analysis(ast).run()
    if analysis.errors:
        raise ParseErrors(*analysis.errors) if len(analysis.errors) > 1 else analysis.errors[0]
