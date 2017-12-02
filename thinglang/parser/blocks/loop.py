from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.lexer.blocks.loops import LexicalRepeatWhile
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class Loop(BaseNode):
    """
    A simple while loop
    """

    def __init__(self, value):
        super(Loop, self).__init__([value])
        self.value = value

    def describe(self):
        return str(self.value)

    def compile(self, context: CompilationBuffer):
        idx = context.current_index + 1
        self.value.compile(context)
        opcode = OpcodeJumpConditional()
        context.append(opcode, self.source_ref)
        super(Loop, self).compile(context)
        context.append(OpcodeJump(idx), self.source_ref)
        opcode.update(context.current_index + 1)

    @staticmethod
    @ParserRule.mark
    def parse_loop(_: LexicalRepeatWhile, value: ValueType):
        return Loop(value)


