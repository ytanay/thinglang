from thinglang.compiler.buffer import CompilationBuffer
from thinglang.lexer.blocks.loops import LexicalRepeatFor
from thinglang.lexer.operators.membership import LexicalIn
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.rule import ParserRule
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.parser.values.named_access import NamedAccess
from thinglang.parser.values.method_call import MethodCall
from thinglang.utils.type_descriptors import ValueType


class IterationLoop(Loop):

    def __init__(self, target: Identifier, target_type: Identifier, collection: ValueType):
        self.target, self.target_type, self.collection = target, target_type, collection
        self.iterator = MethodCall(NamedAccess([collection, "iterator"]))
        super().__init__(MethodCall(NamedAccess([self.iterator, 'has_next']), stack_target=True))

    def finalize(self):
        self.children.insert(0, AssignmentOperation(
            AssignmentOperation.REASSIGNMENT,
            self.target,
            MethodCall(NamedAccess([self.iterator, 'next']), stack_target=True),
            self.target_type
        ).deriving_from(self))

    def compile(self, context: CompilationBuffer):
        self.iterator.compile(context)  # Create the iterator, pushing onto the stack
        super().compile(context)  # Compile the body of the loop

    @staticmethod
    @ParserRule.mark
    def parse_iterative_loop(_1: LexicalRepeatFor, target_type: Identifier, target: Identifier, _2: LexicalIn, collection: ValueType):
        return IterationLoop(target, target_type, collection)
