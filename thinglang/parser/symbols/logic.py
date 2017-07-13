from collections import OrderedDict

from thinglang.compiler import CompilationContext
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.parser.symbols import BaseSymbol


class Conditional(BaseSymbol):

    ADVANCE = False
    SCOPING = True

    def __init__(self, slice):
        super(Conditional, self).__init__(slice)
        _, self.value = slice

        if self.value.implements(Conditional):
            self.value = self.value.value

    def describe(self):
        return 'if {}'.format(self.value)

    def evaluate(self, resolver):
        return self.value.evaluate(resolver)

    def references(self):
        return self.value,

    def transpile(self):
        return 'if({}) {{\n{}\n\t\t}}'.format(self.value.transpile(), self.transpile_children(indent=3))

    def compile(self, context: CompilationContext):
        if not context.conditional_groups or self not in context.conditional_groups[-1]:
            elements = [self] + list(self.siblings_while(lambda x: isinstance(x, ElseBranchInterface)))
            context.conditional_groups.append(OrderedDict((x, None) for x in elements))

        context.push_down(self.value)
        instruction, idx = context.append(OpcodeJumpConditional())
        super(Conditional, self).compile(context)

        if list(context.conditional_groups[-1].keys())[-1] is self:
            context.update_conditional_jumps()
        else:
            jump_out = OpcodeJump()
            context.conditional_groups[-1][self] = jump_out
            context.append(jump_out)

        instruction.update(context.current_index())


class ElseBranchInterface(object):
    SCOPING = True
    pass


class UnconditionalElse(BaseSymbol, ElseBranchInterface):
    def compile(self, context: CompilationContext):
        super(UnconditionalElse, self).compile(context)
        context.update_conditional_jumps()


class ConditionalElse(Conditional, ElseBranchInterface):

    def __init__(self, slice):
        super(ConditionalElse, self).__init__(slice)
        _, self.conditional = slice

    def describe(self):
        return 'otherwise if {}'.format(self.value)

    def references(self):
        return self.conditional.references()


class Loop(BaseSymbol):
    ADVANCE = False
    SCOPING = True

    def __init__(self, slice):
        super(Loop, self).__init__(slice)
        _, self.condition = slice

    def evaluate(self, resolver):
        return self.condition.evaluate(resolver)

    def references(self):
        return self.condition.references()

    def describe(self):
        return str(self.condition)

    def compile(self, context: CompilationContext):
        idx = context.push_down(self.condition)
        jump, _ = context.append(OpcodeJumpConditional())
        super(Loop, self).compile(context)
        context.append(OpcodeJump(idx))
        jump.update(context.current_index())


class IterativeLoop(BaseSymbol):

    EXECUTABLE = False

    def __init__(self, slice):
        super().__init__(slice)
        self.name, self.generator = slice[1], slice[3]

    def describe(self):
        return 'for {self.name} in {self.generator}'
