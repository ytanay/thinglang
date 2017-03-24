from thinglang.lexer.symbols.logic import LexicalEquality
from thinglang.parser.tokens import BaseToken


class Conditional(BaseToken):

    ADVANCE = False
    COMPARATORS = {
        LexicalEquality: lambda lhs, rhs: lhs == rhs
    }

    def __init__(self, slice):
        super(Conditional, self).__init__(slice)
        _, self.lhs, self.comparator, self.rhs = slice
        self.comparator = self.COMPARATORS[type(self.comparator)]

    def describe(self):
        return 'if {} {} {}'.format(self.lhs, self.comparator, self.rhs)

    def evaluate(self, stack):
        return self.comparator(self.lhs.evaluate(stack), self.rhs.evaluate(stack))


class UnconditionalElse(BaseToken):
    pass