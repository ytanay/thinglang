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


class LexicalBoolean(LexicalToken, ValueType):

    @classmethod
    def evaluate(cls, _=None):
        raise NotImplementedError('Must implement evaluate')



class LexicalBooleanTrue(LexicalBoolean):
    STATIC = True

    def transpile(self):
        return 'true'

    @classmethod
    def evaluate(cls, _=None):
        return True

    def serialize(self):
        return LexicalNumericalValue(True).serialize()


class LexicalBooleanFalse(LexicalBoolean):

    def transpile(self):
        return 'false'

    @classmethod
    def evaluate(cls, _=None):
        return False

    def compile(self, context):
        context.append(OpcodePushNull())
