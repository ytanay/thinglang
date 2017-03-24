from thinglang.common import ValueType
from thinglang.lexer.symbols.arithmetic import LexicalAddition, LexicalMultiplication, LexicalSubtraction, \
    LexicalDivision
from thinglang.lexer.symbols.logic import LexicalEquality
from thinglang.parser.tokens import BaseToken


class ArithmeticOperation(BaseToken, ValueType):
    OPERATIONS = {
        LexicalAddition: lambda rhs, lhs: rhs + lhs,
        LexicalMultiplication: lambda rhs, lhs: rhs * lhs,
        LexicalSubtraction: lambda rhs, lhs: rhs - lhs,
        LexicalDivision: lambda rhs, lhs: rhs / lhs,
        LexicalEquality: lambda rhs, lhs: lhs == rhs
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
