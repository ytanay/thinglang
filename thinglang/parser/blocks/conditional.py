from collections import OrderedDict

from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.compiler.tracker import ResolvableIndex
from thinglang.lexer.blocks.conditionals import LexicalConditional
from thinglang.parser.blocks.common import ElseBranchInterface
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class Conditional(BaseNode):
    """
    The base conditional class
    """

    def __init__(self, value):
        super(Conditional, self).__init__([value])
        self.value = value

        if isinstance(self.value, Conditional):
            self.value = self.value.value

    def __repr__(self):
        return 'if {}'.format(self.value)

    def compile(self, context: CompilationBuffer):
        jump_out = ResolvableIndex()
        conditional_jump = OpcodeJumpConditional(jump_out)

        context.jump_out[self] = jump_out

        if not context.conditional_groups or self not in context.conditional_groups[-1]:
            elements = [self] + list(self.siblings_while(lambda x: isinstance(x, ElseBranchInterface)))
            context.conditional_groups.append(OrderedDict((x, None) for x in elements))

        self.value.compile(context)
        context.append(conditional_jump, self.source_ref)
        super(Conditional, self).compile(context)

        if list(context.conditional_groups[-1].keys())[-1] is self:
            context.update_conditional_jumps()
        else:
            jump = OpcodeJump()
            context.conditional_groups[-1][self] = jump
            context.append(jump, self.source_ref)

        jump_out.index = context.next_index

    @staticmethod
    @ParserRule.mark
    def parse_simple_conditional(_: LexicalConditional, value: ValueType):
        return Conditional(value)
