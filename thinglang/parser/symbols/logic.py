from thinglang.compiler import CompilationContext, BytecodeSymbols
from thinglang.lexer.tokens.logic import LexicalEquality
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
        context.push_down(self.value)
        instruction, idx = context.append(BytecodeSymbols.conditional_jump())
        super(Conditional, self).compile(context)
        if self.next_sibling().implements(UnconditionalElse):
            context.append(BytecodeSymbols.jump())
        instruction.args = context.current_index() - idx,


class ElseBranchInterface(object):
    SCOPING = True
    pass


class UnconditionalElse(BaseSymbol, ElseBranchInterface):
    def compile(self, context: CompilationContext):
        jump, idx = context.last()
        super(UnconditionalElse, self).compile(context)
        jump.args = context.current_index() - idx,


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


class IterativeLoop(BaseSymbol):

    EXECUTABLE = False

    def __init__(self, slice):
        super().__init__(slice)
        self.name, self.generator = slice[1], slice[3]

    def describe(self):
        return 'for {self.name} in {self.generator}'
