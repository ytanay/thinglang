from thinglang.lexer.tokens import LexicalToken
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import BaseSymbol
from thinglang.utils.type_descriptors import ValueType


class AssignmentOperation(BaseSymbol):
    DECELERATION = object()
    REASSIGNMENT = object()
    INDETERMINATE = object()

    def __init__(self, slice):
        super(AssignmentOperation, self).__init__(slice)
        if len(slice) == 4:
            _1, self.name, _2, self.value = slice
            self.name.type = slice[0]
            self.intent = self.DECELERATION
        else:
            self.name, _, self.value = slice
            self.intent = self.REASSIGNMENT

    def describe(self):
        return '{} = {}'.format(self.name, self.value)

    def references(self):
        return (self.name, self.value.references()) if self.intent is self.REASSIGNMENT else self.value.references()

    @classmethod
    def create(cls, name, value, type=None):
        return cls(([type] if type is not None else []) + [name, None, value])

    def transpile(self):
        if self.intent is self.DECELERATION:
            return '{} {} = {};'.format(self.name.type.transpile(), self.name.transpile(), self.value.transpile())
        elif self.intent is self.REASSIGNMENT:
            return '{} = {};'.format(self.name.transpile(), self.value.transpile())


class InlineString(LexicalToken, ValueType):  # immediate string e.g. "hello world"
    TYPE = LexicalIdentifier("text")

    def __init__(self, value):
        super().__init__(None)
        self.value = value

    def evaluate(self, _):
        return self.value

    def serialize(self):
        return self.evaluate(None)

    def references(self):
        return ()

    def transpile(self):
        return f'"{self.value}"'

    def type(self):
        return self.TYPE
