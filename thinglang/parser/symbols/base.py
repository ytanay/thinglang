from thinglang.parser.symbols import BaseSymbol
from thinglang.utils.type_descriptors import ValueType


class AssignmentOperation(BaseSymbol):
    DECELERATION = object()
    REASSIGNMENT = object()
    INDETERMINATE = object()

    def __init__(self, slice):
        super(AssignmentOperation, self).__init__(slice)
        if len(slice) == 4:
            self.type, self.name, _, self.value = slice
            self.intent = self.DECELERATION
        else:
            self.name, _, self.value = slice
            self.intent = self.REASSIGNMENT
            self.type = self.INDETERMINATE

    def describe(self):
        return '{} {} = {}'.format(self.type, self.name, self.value)

    def references(self):
        return (self.name, self.value.references()) if self.intent is self.REASSIGNMENT else self.value.references()

    @classmethod
    def create(cls, name, value, type=None):
        return cls(([type] if type is not None else []) + [name, None, value])

    def transpile(self):
        if self.intent is self.DECELERATION:
            return '{} {} = {};'.format(self.type.transpile(), self.name.transpile(), self.value.transpile())
        elif self.intent is self.REASSIGNMENT:
            return '{} = {};'.format(self.name.transpile(), self.value.transpile())


class InlineString(ValueType):  # immediate string e.g. "hello world"
    def __init__(self, value):
        self.value = value

    def evaluate(self, _):
        return self.value

    def serialize(self):
        return self.evaluate(None)

    def references(self):
        return ()

    def transpile(self):
        return f'"{self.value}"'