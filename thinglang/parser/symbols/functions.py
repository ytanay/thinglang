from thinglang.compiler.opcodes import OpcodeCallInternal, OpcodeCall, OpcodePop, OpcodeReturn
from thinglang.lexer.tokens.base import LexicalAccess, LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalClassInitialization
from thinglang.parser.symbols import BaseSymbol
from thinglang.parser.symbols.collections import ListInitializationPartial, ListInitialization
from thinglang.utils.type_descriptors import ValueType


class Access(BaseSymbol):
    def __init__(self, slice):
        super(Access, self).__init__(slice)
        self.target = [x for x in slice if not isinstance(x, LexicalAccess)]
        self.type = None

    def evaluate(self, resolver):
        return resolver.resolve(self)

    def describe(self):
        return '{}:{}'.format('.'.join(str(x) for x in self.target), self.type)

    def __getitem__(self, item):
        return self.target[item]

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target

    @classmethod
    def create(cls, target):
        return cls([LexicalIdentifier(x) if not isinstance(x, LexicalIdentifier) else x for x in target])

    def transpile(self):
        return '->'.join(x.transpile() for x in self.target)

    def type_id(self):
        return None


class ArgumentListPartial(ListInitializationPartial):
    pass


class ArgumentListDecelerationPartial(ArgumentListPartial):
    STRICTLY_TYPED = True
    pass


class ArgumentList(ListInitialization):
    pass


class MethodCall(BaseSymbol, ValueType):
    def __init__(self, slice):
        super(MethodCall, self).__init__(slice)
        self.value = self

        if isinstance(slice[0], LexicalClassInitialization):
            self.target = Access([slice[1], LexicalIdentifier.constructor().set_context(slice[0])])
            self.arguments = slice[2]
            self.constructing_call = True
        else:
            self.target, self.arguments = slice
            self.constructing_call = False

        if not self.arguments:
            self.arguments = ArgumentList()

        self.resolved_target = None
        self.internal = False

    def describe(self):
        return 'target={}, args={}'.format(self.target, self.arguments)

    def replace(self, original, replacement):
        self.arguments.replace(original, replacement)

    def references(self):
        return self.target, self.arguments

    @classmethod
    def create_constructing_call(cls, target, arguments=None):
        return cls([LexicalClassInitialization(None), target, arguments if arguments is not None else ArgumentList()])

    @classmethod
    def create(cls, target, arguments=None):
        return cls([Access.create(target), arguments])

    def transpile(self, orphan=True):
        return f'{self.target.transpile()}({self.arguments.transpile()}){";" if orphan else ""}'

    def statics(self):
        yield from self.arguments.statics()

    def compile(self, context, captured=False):

        for arg in reversed(self.arguments):
            context.push_down(arg)

        if self.internal:
            context.append(OpcodeCallInternal(*self.resolved_target.index))
        else:
            context.append(OpcodeCall(*self.resolved_target.index))

        if not captured:
            context.append(OpcodePop())  # pop the return value, if the return value is not captured

    def type_id(self):
        return self.resolved_target.type


class ReturnStatement(BaseSymbol):
    def __init__(self, slice):
        super().__init__(slice)
        self.value = slice[1] if len(slice) == 2 else None

    def transpile(self):
        if self.value:
            return 'return Thing(new this_type({}));'.format(self.value.transpile())
        else:
            return 'return NULL;'

    def compile(self, context):
        context.push_down(self.value)
        context.append(OpcodeReturn())