from collections import OrderedDict

from thinglang.compiler import CompilationContext
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.parser.nodes import BaseNode


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
        return 'if({}) {{\n{}\n\t\t}}'.format(self.value.transpile(), self.transpile_children(indent=3))

    def compile(self, context: CompilationContext):
        if not context.conditional_groups or self not in context.conditional_groups[-1]:
            elements = [self] + list(self.siblings_while(lambda x: isinstance(x, ElseBranchInterface)))
            context.conditional_groups.append(OrderedDict((x, None) for x in elements))

        self.value.compile(context)
        opcode = OpcodeJumpConditional()
        context.append(opcode)
        super(Conditional, self).compile(context)

        if list(context.conditional_groups[-1].keys())[-1] is self:
            context.update_conditional_jumps()
        else:
            jump_out = OpcodeJump()
            context.conditional_groups[-1][self] = jump_out
            context.append(jump_out)

        opcode.update(context.current_index())


class ElseBranchInterface(object):
    SCOPING = True
    pass


class UnconditionalElse(BaseNode, ElseBranchInterface):
    def compile(self, context: CompilationContext):
        super(UnconditionalElse, self).compile(context)
        context.update_conditional_jumps()

    def transpile(self):
        return 'else {{\n{}\n\t\t}}'.format(self.transpile_children(indent=3))


class ConditionalElse(Conditional, ElseBranchInterface):

    def __init__(self, slice):
        super(ConditionalElse, self).__init__(slice)
        _, self.conditional = slice

    def describe(self):
        return 'otherwise if {}'.format(self.value)


class Loop(BaseNode):
    ADVANCE = False
    SCOPING = True

    def __init__(self, slice):
        super(Loop, self).__init__(slice)
        _, self.value = slice

    def describe(self):
        return str(self.value)

    def compile(self, context: CompilationContext):
        idx = context.current_index()
        self.value.compile(context)
        opcode = OpcodeJumpConditional()
        context.append(opcode)
        super(Loop, self).compile(context)
        context.append(OpcodeJump(idx))
        opcode.update(context.current_index())
