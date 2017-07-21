import itertools

from thinglang.compiler.allocation import LinearMemoryAllocationLayout
from thinglang.compiler.references import ResolvedReference
from thinglang.foundation import Foundation
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import BaseNode, Transient
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import ThingDefinition, MethodDefinition
from thinglang.parser.symbols.functions import MethodCall, ReturnStatement
from thinglang.utils import collection_utils
from thinglang.utils.tree_utils import TreeTraversal, inspects
from thinglang.utils.union_types import ACCESS_TYPES


class IndexerContext(object):
    def __init__(self):
        self.instance_members, self.locals, self.current_method, self.current_thing = None, None, None, None
        self.things = []

    def over(self, thing_definition):
        self.current_thing = thing_definition
        self.things.append(thing_definition)
        self.instance_members = {
            member.name: (idx, member) for idx, member in enumerate(thing_definition.members())
        }

    def set_last_frame_size(self, size):
        if self.current_method:
            self.current_method.frame_size = size

    def set_method(self, node):
        self.current_method = node


class Collator(TreeTraversal):

    def __init__(self, ast):
        super(Collator, self).__init__(ast)
        self.thing_counter = itertools.count(0)
        self.method_counter = None
        self.current_thing_index = None

    @inspects(ThingDefinition)
    def set_thing_context(self, node: ThingDefinition) -> None:
        self.current_thing_index = node.index = next(self.thing_counter)
        node.finalize()
        self.method_counter = itertools.count(0)

    @inspects(MethodDefinition)
    def set_method_context(self, node: MethodDefinition) -> None:
        node.index = self.current_thing_index, next(self.method_counter)


class Indexer(TreeTraversal):

    def __init__(self, ast):
        super().__init__(ast)
        self.context = IndexerContext()
        self.locals = None

    def run(self):
        super(Indexer, self).run()
        self.context.set_last_frame_size(self.locals.next_index)

    @inspects(ThingDefinition)
    def set_thing_context(self, node: ThingDefinition) -> None:
        self.context.over(node)

    @inspects(MethodDefinition)
    def set_method_context(self, node: MethodDefinition) -> None:
        if self.locals:
            self.context.set_last_frame_size(self.locals.next_index)

        self.context.set_method(node)
        self.locals = LinearMemoryAllocationLayout({
            argument: (idx, argument.type) for idx, argument in enumerate(node.arguments)
        })

    @inspects(AssignmentOperation, priority=1)
    def process_assignment_operation(self, node: AssignmentOperation) -> None:

        if node.value.implements(MethodCall):
            self.inspect_method_call(node.value)

        if node.name.implements(Transient):
            node.name.type = node.value.type_id()

        if node.intent is AssignmentOperation.DECELERATION:
            self.process_declaration(node)
        elif node.intent is AssignmentOperation.REASSIGNMENT:
            self.process_assignment(node)

    @inspects(object)
    def process_reference_dependencies(self, node: BaseNode):
        for x in collection_utils.emit_recursively(node.references(), ACCESS_TYPES):
            if x.implements(LexicalIdentifier):
                x.index, x.type = self.locals.get(x)

    @inspects(MethodCall)
    def inspect_method_call(self, node: MethodCall) -> None:
        """
        The reference indexing for method calls involves 2 separate processes - resolving the method target,
        and resolving each argument in turn
        """

        node.arguments = [
            arg if arg.STATIC else ResolvedReference(*self.locals.get(arg)) for arg in node.arguments
        ]

        if node.target[0] in Foundation().types:
            assert len(node.target.target) == 2
            type_id = node.target[0]

            node.resolved_target = ResolvedReference((
                Foundation().INTERNAL_TYPE_ORDERING[type_id],
                Foundation().type(type_id).index(node.target[1].transpile())),
                None)  # TODO: fix None

            node.internal = True
            return

        if node.target[0].is_self():
            target = self.context.current_thing
        elif self.ast.get(node.target[0]):
            print('{} refers to a user class'.format(node.target))
            target = self.ast.get(node.target[0])
        else:
            raise Exception('Cannot resolve {}'.format(node.target))

        for x in node.target[1:]:
            print('Target {}, x: {} {}'.format(target, x, target.index))
            target = target[x]
        node.resolved_target = ResolvedReference(target.index, target.type_id())

    @inspects(ReturnStatement)
    def inspect_return_statement(self, node: ReturnStatement) -> None:
        if node.value is not None:
            node.value = node.value if node.value.STATIC else ResolvedReference(*self.locals.get(node.value), original=node.value)

    def process_declaration(self, node):
        if node in self.locals:
            raise Exception('Duplicate declaration')
        else:
            node.target = self.locals.add(node.name)

    def process_assignment(self, node: AssignmentOperation):
        if node.name.implements(LexicalIdentifier):
            node.target = self.locals.get(node.name)
        else:
            raise Exception('cannot resolve references yet!')
