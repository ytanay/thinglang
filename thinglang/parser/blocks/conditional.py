from collections import OrderedDict

from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.foundation import templates
from thinglang.lexer.blocks.conditionals import LexicalConditional
from thinglang.parser.blocks.common import ElseBranchInterface
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class Conditional(BaseNode):

    def __init__(self, value):
        super(Conditional, self).__init__([value])
        self.value = value

        if isinstance(self.value, Conditional):
            self.value = self.value.value

    def describe(self):
        return 'if {}'.format(self.value)

    def transpile(self):
        return templates.CONDITIONAL.format(
            prefix='',
            condition=self.value.transpile(),
            body=self.transpile_children(indent=3)
        )

    def compile(self, context: CompilationBuffer):
        if not context.conditional_groups or self not in context.conditional_groups[-1]:
            elements = [self] + list(self.siblings_while(lambda x: isinstance(x, ElseBranchInterface)))
            context.conditional_groups.append(OrderedDict((x, None) for x in elements))

        self.value.compile(context)
        opcode = OpcodeJumpConditional()
        context.append(opcode, self.source_ref)
        super(Conditional, self).compile(context)

        if list(context.conditional_groups[-1].keys())[-1] is self:
            context.update_conditional_jumps()
        else:
            jump_out = OpcodeJump()
            context.conditional_groups[-1][self] = jump_out
            context.append(jump_out, self.source_ref)

        opcode.update(context.current_index + 1)

    @staticmethod
    @ParserRule.mark
    def parse_simple_conditional(_: LexicalConditional, value: ValueType):
        return Conditional(value)
