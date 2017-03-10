from thinglang.common import Describeable, ValueType
from thinglang.lexer.lexical_tokens import LexicalIdentifier


class BaseToken(Describeable):
    BLOCK = False

    def __init__(self, slice):
        self.children = []
        self.indent = 0
        self.value = None
        self.raw_slice = slice
        if slice:
            self.context = slice[0].context

    def attach(self, child):
        self.children.append(child)
        child.parent = self

    def find(self, name):
        for child in self.children:
            if child.value == name:
                return child

    def tree(self, depth=1):
        separator = ('\n' if self.children else '') + ('\t' * depth)
        return '{}({}){}{}'.format(type(self).__name__, self.describe(), separator,
                                   separator.join(child.tree(depth=depth + 1) for child in self.children))

    def describe(self):
        return self.value if self.value is not None else ''


class RootToken(BaseToken):
    BLOCK = True


class DefinitionPairToken(BaseToken):
    def __init__(self, slice):
        super(DefinitionPairToken, self).__init__(slice)
        self.value = slice[1].value


class ThingDefinition(DefinitionPairToken): pass


class MethodDefinition(DefinitionPairToken):
    def __init__(self, slice):
        super(MethodDefinition, self).__init__(slice)

        if isinstance(slice[2], ArgumentList):
            self.arguments = slice[2].value
        else:
            self.arguments = []

    def describe(self):
        return '{}, args={}'.format(self.value, self.arguments)


class Pointer(BaseToken): pass


class Access(Pointer):
    def __init__(self, slice):
        super(Access, self).__init__(slice)
        self.value = [x.value for x in slice if isinstance(x, LexicalIdentifier)]


class String(ValueType):
    def __init__(self, value):
        self.value = value

    def evaluate(self, stack):
        return self.value


class ArgumentListPartial(BaseToken):
    def __init__(self, slice):
        super(ArgumentListPartial, self).__init__(slice)
        if isinstance(slice[0], ArgumentListPartial):
            self.value = slice[0].value + [slice[2]]
        else:
            self.value = [slice[1]]


class ArgumentList(BaseToken):
    def __init__(self, slice):
        super(ArgumentList, self).__init__(slice)
        if isinstance(slice[0], ArgumentListPartial):
            self.value = slice[0].value
        else:
            self.value = []

    def evaluate(self, stack):
        return [value.evaluate(stack) for value in self.value]


class ProcessedIndent(BaseToken):
    def __init__(self, size, slice):
        super(ProcessedIndent, self).__init__(slice)
        self.value = size


class MethodCall(BaseToken):
    def __init__(self, slice):
        super(MethodCall, self).__init__(slice)
        self.target, self.arguments = slice

        if not self.arguments:
            self.arguments = []

    def describe(self):
        return 'target={}, args={}'.format(self.target, self.arguments)


class ArithmeticOperation(BaseToken, ValueType):
    OPERATIONS = {
        "+": lambda rhs, lhs: rhs + lhs,
        "*": lambda rhs, lhs: rhs * lhs,
        "-": lambda rhs, lhs: rhs - lhs,
        "/": lambda rhs, lhs: rhs / lhs
    }

    def __init__(self, slice):
        super(ArithmeticOperation, self).__init__(slice)
        self.lhs, self.operator, self.rhs = slice

    def evaluate(self, stack):
        return self.OPERATIONS[self.operator.operator](self.lhs.evaluate(stack), self.rhs.evaluate(stack))


class ArithmeticAdd(BaseToken):
    def evaluate(self, left, right):
        return left.evaluate() + right.evaluate()


class AssignmentOperation(BaseToken):
    DECELERATION = object()
    REASSIGNMENT = object()

    def __init__(self, slice):
        super(AssignmentOperation, self).__init__(slice)
        if len(slice) == 4:
            self.type, self.name, _, self.value = slice
            self.method = self.DECELERATION
        else:
            self.name, _, self.value = slice
            self.method = self.REASSIGNMENT
            self.type = 'INDETERMINATE'

    def describe(self):
        return '{} {} = {}'.format(self.type, self.name, self.value)

    def execute(self, stack):
        if self.method is self.DECELERATION:
            assert self.name.value not in stack, 'variable {} declaration but was found in stack'.format(self.name.value)
        else:
            assert self.name.value in stack, 'variable {} reassignment but is not in stack {}'.format(self.name.value, self.context)

        stack[self.name.value] = self.value.evaluate(stack)


class ReturnStatement(DefinitionPairToken):
    def __init__(self, slice):
        super().__init__(slice)
        self.value = slice[1]