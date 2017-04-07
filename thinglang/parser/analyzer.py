import types

from thinglang.execution.builtins import BUILTINS, INTERNAL_MEMBER
from thinglang.execution.errors import ReturnInConstructorError, EmptyMethodBody, EmptyThingDefinition, \
    ArgumentCountMismatch, UnresolvedReference, DuplicateDeclaration
from thinglang.execution.resolver import Resolver
from thinglang.execution.stack import Frame
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.errors import ParseErrors
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import MethodDefinition, ThingDefinition
from thinglang.parser.symbols.functions import ReturnStatement, MethodCall, Access
from thinglang.utils.collection_utils import emit_recursively
from thinglang.utils.tree_utils import inspects
from thinglang.utils.union_types import ACCESS_TYPES


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

        if self.errors:
            raise ParseErrors(*self.errors) if len(self.errors) > 1 else self.errors[0]

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

    def inspect(self, node):
        for inspection in self.inspections:
            if not inspection.inspected_types or isinstance(node, inspection.inspected_types):
                result = inspection(node)
                if isinstance(result, types.GeneratorType):
                    self.errors.extend(result)

    def report_exception(self, error):
        self.errors.append(error)

    def normalize_reference_access(self, access):
        if access.implements(LexicalIdentifier):
            return access
        target = access[0] if access[0].is_self() or access[0] not in self.scoping else self.scoping[access[0]]
        return Access([target] + access[1:])

    @inspects()
    def verify_reference_dependencies(self, node):
        refs = emit_recursively(node.references(), ACCESS_TYPES)

        for ref in (x for x in refs if self.resolver.lookup(self.normalize_reference_access(x)) is Resolver.UNRESOLVED_REFERENCE):
            yield UnresolvedReference(ref)

    @inspects(AssignmentOperation)
    def mark_variable_deceleration(self, node):
        if node.name.implements(LexicalIdentifier):
            if node.method is AssignmentOperation.DECELERATION:
                if self.resolver.lookup(node.name) is not Resolver.UNRESOLVED_REFERENCE:
                    yield DuplicateDeclaration(node.name)
                else:
                    self.scoping[node.name] = node.type
        elif self.resolver.lookup(self.normalize_reference_access(node.name)) is Resolver.UNRESOLVED_REFERENCE:
            yield UnresolvedReference(node.name)

    @inspects(MethodCall)
    def verify_method_call_arity(self, node):
        definition = self.resolver.lookup(self.normalize_reference_access(node.target))
        if definition not in (INTERNAL_MEMBER, Resolver.UNRESOLVED_REFERENCE) and len(definition.arguments) != len(node.arguments):
            yield ArgumentCountMismatch(expected=len(definition.arguments), actual=len(node.arguments))

    @inspects(ThingDefinition)
    def verify_thing_definitions(self, node):
        self.scoping.instance = node

        if not node.children:
            yield EmptyThingDefinition()

    @inspects(MethodDefinition)
    def verify_method_definitions(self, node):
        self.scoping.reset({
            x: True for x in node.arguments
        })

        if not node.children:
            yield EmptyMethodBody()

        if node.is_constructor() and list(node.find(lambda x: isinstance(x, ReturnStatement))):
            yield ReturnInConstructorError(node)
