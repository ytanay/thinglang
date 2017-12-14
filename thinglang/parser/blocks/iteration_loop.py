import itertools

from thinglang.compiler.buffer import CompilationBuffer
from thinglang.lexer.blocks.loops import LexicalRepeatFor
from thinglang.lexer.operators.membership import LexicalIn
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.rule import ParserRule
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.parser.values.method_call import MethodCall
from thinglang.parser.values.named_access import NamedAccess
from thinglang.utils.type_descriptors import ValueType


class IterationLoop(Loop):

    TRANSIENT_COUNTER = itertools.count()

    def __init__(self, target: Identifier, target_type: Identifier, collection: ValueType):
        super().__init__(None, (target, target_type, collection))

        self.target, self.target_type, self.collection = target, target_type, collection
        self.iterator_id = next(IterationLoop.TRANSIENT_COUNTER)

        self.iterator = self.iterator_container_name[0]
        self.continuation_check = MethodCall(NamedAccess([self.iterator, Identifier('has_next')])).deriving_from(self)
        self.continuation_next = MethodCall(NamedAccess([self.iterator, Identifier('next')])).deriving_from(self)

        self.value = self.continuation_check

    def __repr__(self):
        return f'for {self.target_type} {self.target} in {self.collection}'

    def compile(self, context: CompilationBuffer):
        iterator_name, iterator_type = self.iterator_container_name
        AssignmentOperation(
            AssignmentOperation.REASSIGNMENT,
            iterator_name,
            MethodCall(NamedAccess([self.collection, Identifier('iterator')])).deriving_from(self),
            iterator_type
        ).deriving_from(self).compile(context)

        super().compile(context)

    def finalize(self):
        self.children.insert(0, AssignmentOperation(
            AssignmentOperation.DECELERATION,
            self.target,
            self.continuation_next,
            self.target_type
        ).deriving_from(self))

    @staticmethod
    @ParserRule.mark
    def parse_iterative_loop(_1: LexicalRepeatFor, target_type: Identifier, target: Identifier, _2: LexicalIn, collection: ValueType):
        return IterationLoop(target, target_type, collection)

    @property
    def iterator_container_name(self):
        return Identifier(f'__iteration_loop_container_{self.iterator_id}__'), GenericIdentifier(Identifier('iterator'), (self.target_type,))