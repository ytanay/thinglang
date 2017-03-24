import abc

from thinglang.common import ValueType
from thinglang.lexer.symbols import LexicalSymbol


class LexicalComparison(LexicalSymbol, metaclass=abc.ABCMeta):  # one of eq, neq, >, <, etc...
    pass


class LexicalConditional(LexicalSymbol):  # if conditional
    pass


class LexicalElse(LexicalSymbol):  # otherwise
    pass


class LexicalEquality(LexicalComparison):  # lhs eq rhs
    pass


class LexicalInequality(LexicalComparison):
    pass


class LexicalNegation(LexicalSymbol):
    pass


class LexicalGreaterThan(LexicalComparison):
    pass


class LexicalLessThan(LexicalComparison):
    pass


class LexicalBoolean(LexicalSymbol, ValueType):
    pass


class LexicalBooleanTrue(LexicalBoolean):
    def evaluate(self, stack):
        return True


class LexicalBooleanFalse(LexicalBoolean):
    def evaluate(self, stack):
        return False