import abc

from thinglang.utils.describable import Describable


class LexicalToken(Describable):
    EMITTABLE = True
    STATIC = False
    ALLOW_EMPTY = False
    MUST_CLOSE = False

    def __init__(self, value, source_ref):
        self.value, self.source_ref = value, source_ref

    @classmethod
    def next_operator_set(cls, current, original):
        return current

    def transpile(self):
        return self.value

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.value == other.value

    def __hash__(self):
        return hash((type(self), self.value))


class LexicalBinaryOperation(LexicalToken):
    def __init__(self, value, source_ref):
        super(LexicalBinaryOperation, self).__init__(value, source_ref)
        self.operator = value

    @classmethod
    def transpile(cls):
        return '__{}__'.format(cls.__name__)


class LexicalGroupEnd(LexicalToken):
    def __init__(self):
        super(LexicalGroupEnd, self).__init__(None, None)
