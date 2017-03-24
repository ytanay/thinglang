from thinglang.lexer.symbols.logic import LexicalEquality
from thinglang.parser.tokens import BaseToken


class Conditional(BaseToken):

    ADVANCE = False

    def __init__(self, slice):
        super(Conditional, self).__init__(slice)
        _, self.value = slice

    def describe(self):
        return 'if {}'.format(self.value)

    def evaluate(self, stack):
        return self.value.evaluate(stack)


class ElseBranchInterface(object):
    pass


class UnconditionalElse(BaseToken, ElseBranchInterface):
    pass


class ConditionalElse(Conditional, ElseBranchInterface):

    def __init__(self, slice):
        super(ConditionalElse, self).__init__(slice)
        _, self.conditional = slice

    def describe(self):
        return 'otherwise if {}'.format(self.value)