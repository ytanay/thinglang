from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.compiler.tracker import ResolvableIndex
from thinglang.lexer.blocks.loops import LexicalRepeatWhile
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class Loop(BaseNode):
    """
    A simple while loop
    """

    def __init__(self, value, original_tokens=()):
        super(Loop, self).__init__((value,) + original_tokens)
        self.value = value

    def __repr__(self):
        return str(self.value)

    def compile(self, context: CompilationBuffer):
        loop_start = ResolvableIndex(context.next_index) # Jumps to the evaluation of the loop's expression
        jump_out = ResolvableIndex()  # Jumps out of the loop when done
        conditional_jump = OpcodeJumpConditional(jump_out)

        context.jump_out[self] = jump_out
        context.jump_in[self] = loop_start

        self.value.compile(context)
        context.append(conditional_jump, self.source_ref) # Evaluation

        super(Loop, self).compile(context)

        context.append(OpcodeJump(loop_start.index), self.source_ref)
        jump_out.index = context.next_index

    @staticmethod
    @ParserRule.mark
    def parse_loop(_: LexicalRepeatWhile, value: ValueType):
        return Loop(value)


