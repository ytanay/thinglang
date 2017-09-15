from collections import OrderedDict

from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.foundation import templates
from thinglang.parser.nodes import BaseNode
from thinglang.parser.nodes.blocks.common import ElseBranchInterface


class Conditional(BaseNode):

    ADVANCE = False
    SCOPING = True

    def __init__(self, slice):
        super(Conditional, self).__init__(slice)
        _, self.value = slice

        if self.value.implements(Conditional):
            self.value = self.value.value

    def describe(self):
        return 'if {}'.format(self.value)

    def transpile(self):
        return templates.CONDITIONAL.format(
            condition=self.value.transpile(),
            body=self.transpile_children(indent=3)
        )

    def compile(self, context: CompilationContext):
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

        opcode.update(context.current_index())
