import types

from thinglang.execution.builtins import BUILTINS, INTERNAL_MEMBER
from thinglang.execution.resolver import Resolver
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.errors import ParseErrors, UnresolvedReference, DuplicateDeclaration, ReturnInConstructorError, \
    EmptyMethodBody, EmptyThingDefinition, IndeterminateType, ArgumentCountMismatch
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import MethodDefinition, ThingDefinition
from thinglang.parser.symbols.functions import ReturnStatement, MethodCall, Access
from thinglang.utils import collection_utils
from thinglang.utils.collection_utils import emit_recursively
from thinglang.utils.tree_utils import inspects, TreeTraversal
from thinglang.utils.union_types import ACCESS_TYPES


class Analyzer(TreeTraversal):
    def __init__(self, ast):
        super(Analyzer, self).__init__(ast)
        self.resolver = Resolver(self.scoping, collection_utils.combine({
            LexicalIdentifier(x.INTERNAL_NAME): x.EXPORTS for x in BUILTINS
        }, {
            x.name: x for x in self.ast.children
        }))

    def run(self):
        super().run()

        if self.results:
            raise ParseErrors(*self.results) if len(self.results) > 1 else self.results[0]

        return self

    def inspect(self, node, parent):
        assert node.parent is parent, 'expected node {} to have parent {} but got {}'.format(node, parent, node.parent)
        super().inspect(node, parent)

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
            if node.method is AssignmentOperation.DECELERATION:  # Decelerations must be strongly typed
                if self.resolver.lookup(node.name) is not Resolver.UNRESOLVED_REFERENCE:
                    yield DuplicateDeclaration(node.name)
                else:
                    self.scoping[node.name] = node.type
            elif node.name in self.scoping:
                node.type = self.scoping[node.name]
        else:
            member_ref = self.resolver.lookup(self.normalize_reference_access(node.name))
            if member_ref is Resolver.UNRESOLVED_REFERENCE:
                yield UnresolvedReference(node.name)
            else:
                node.type = member_ref.type

        if not list(self.verify_reference_dependencies(node)) and node.type is AssignmentOperation.INDETERMINATE:
            yield IndeterminateType(node)

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
