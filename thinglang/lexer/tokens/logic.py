from thinglang.compiler.opcodes import OpcodePushNull
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue
from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalToken


class LexicalComparison(LexicalToken):  # one of eq, neq, >, <, etc...

    @classmethod
    def transpile(cls):
        return '__{}__'.format(cls.__name__)


class LexicalConditional(LexicalToken):  # if conditional
    pass


class LexicalElse(LexicalToken):  # otherwise
    pass


class LexicalRepeat(LexicalToken):
    EMITTABLE = False

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'while': LexicalRepeatWhile, 'for': LexicalRepeatFor}
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


class LexicalIn(LexicalToken):
    pass


class LexicalRepeatFor(LexicalToken):
    pass


class LexicalBoolean(LexicalNumericalValue):
    pass


class LexicalBooleanTrue(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanTrue, self).__init__(True, source_ref)


class LexicalBooleanFalse(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanFalse, self).__init__(False, source_ref)

