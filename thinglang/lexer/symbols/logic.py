import abc

from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.symbols import LexicalSymbol


class LexicalComparison(LexicalSymbol, metaclass=abc.ABCMeta):  # one of eq, neq, >, <, etc...
    pass


class LexicalConditional(LexicalSymbol):  # if conditional
    pass


class LexicalElse(LexicalSymbol):  # otherwise
    pass


class LexicalRepeat(LexicalSymbol):
    EMITTABLE = False

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'while': LexicalRepeatWhile}
        return original


class LexicalRepeatWhile(LexicalSymbol):  # repeat while
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
    def evaluate(self, stack):
        raise NotImplementedError('Must implement evaluate')


class LexicalBooleanTrue(LexicalBoolean):
    def evaluate(self, stack):
        return True


class LexicalBooleanFalse(LexicalBoolean):
    def evaluate(self, stack):
        return False