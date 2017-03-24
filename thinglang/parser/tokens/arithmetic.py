from thinglang.common import ValueType
from thinglang.lexer.symbols.arithmetic import LexicalAddition, LexicalMultiplication, LexicalSubtraction, \
    LexicalDivision
from thinglang.lexer.symbols.logic import LexicalEquality, LexicalInequality, LexicalGreaterThan, LexicalLessThan
from thinglang.parser.tokens import BaseToken


class ArithmeticOperation(BaseToken, ValueType):
    OPERATIONS = {
        LexicalAddition: lambda lhs, rhs: lhs + rhs,
        LexicalMultiplication: lambda lhs, rhs: lhs * rhs,
        LexicalSubtraction: lambda lhs, rhs: lhs - rhs,
        LexicalDivision: lambda lhs, rhs: lhs / rhs,
        LexicalEquality: lambda lhs, rhs: lhs == rhs,
        LexicalInequality: lambda lhs, rhs: lhs != rhs,
    }

    def __init__(self, slice):
        super(ArithmeticOperation, self).__init__(slice)
        self.arguments = [slice[0], slice[2]]
        self.operator = type(slice[1])

    def evaluate(self, stack):
        return self.OPERATIONS[self.operator](self[0].evaluate(stack), self[1].evaluate(stack))

    def describe(self):
        return '|{} {} {}|'.format(self[0], self.operator, self[1])

    def replace_argument(self, original, replacement):
        self.arguments = [replacement if x is original else x for x in self.arguments]

    def __getitem__(self, item):
        return self.arguments[item]
