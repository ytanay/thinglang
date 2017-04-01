import abc

from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalToken


class LexicalComparison(LexicalToken, metaclass=abc.ABCMeta):  # one of eq, neq, >, <, etc...
    pass


class LexicalConditional(LexicalToken):  # if conditional
    pass


class LexicalElse(LexicalToken):  # otherwise
    pass


class LexicalRepeat(LexicalToken):
    EMITTABLE = False

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'while': LexicalRepeatWhile}
        return original


class LexicalRepeatWhile(LexicalToken):  # repeat while
    pass


class LexicalEquality(LexicalComparison):  # lhs eq rhs
    pass


class LexicalInequality(LexicalComparison):
    pass


class LexicalNegation(LexicalToken):
    pass


class LexicalGreaterThan(LexicalComparison):
    pass


class LexicalLessThan(LexicalComparison):
    pass


class LexicalBoolean(LexicalToken, ValueType):
    def evaluate(self, _):
        raise NotImplementedError('Must implement evaluate')


class LexicalBooleanTrue(LexicalBoolean):
    def evaluate(self, _):
        return True


class LexicalBooleanFalse(LexicalBoolean):
    def evaluate(self, _):
        return False
