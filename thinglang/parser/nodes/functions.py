from thinglang.compiler.opcodes import OpcodeCallInternal, OpcodeCall, OpcodePop, OpcodeReturn
from thinglang.compiler.references import ElementReference
from thinglang.lexer.tokens.base import LexicalAccess, LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalClassInitialization
from thinglang.parser.nodes import BaseNode
from thinglang.parser.nodes.collections import ListInitializationPartial, ListInitialization
from thinglang.symbols.symbol import Symbol
from thinglang.utils.type_descriptors import ValueType


class Access(BaseNode, ValueType):
    def __init__(self, slice):
        super(Access, self).__init__(slice)
        self.target = [x for x in slice if not isinstance(x, LexicalAccess)]
        self.type = None
        self.arguments = []

    def evaluate(self, resolver):
        return resolver.resolve(self)

    def describe(self):
        return '{}:{}'.format('.'.join(str(x) for x in self.target), self.type)

    def split(self):
        return self.target[:2], self.target[2:]

    def __getitem__(self, item):
        return self.target[item]

    def __eq__(self, other):
        return type(self) == type(other) and self.target == other.target

    def __len__(self):
        size = len(self.target)
        assert size >= 2
        return size

    def transpile(self):
        return '->'.join(x.transpile() for x in self.target)

    def type_id(self):
        return None

    def partial(self, idx):
        return Access(*self.target[idx:idx+2])


class ArgumentListPartial(ListInitializationPartial):
    pass


class ArgumentListDecelerationPartial(ArgumentListPartial):
    STRICTLY_TYPED = True
    pass


class ArgumentList(ListInitialization):
    pass


class MethodCall(BaseNode, ValueType):
    def __init__(self, slice):
        super(MethodCall, self).__init__(slice)

        if isinstance(slice[0], LexicalClassInitialization):
            self.target = Access([slice[1], LexicalIdentifier.constructor().set_context(slice[0])])
            self.arguments = ArgumentList(slice[2])
            self.constructing_call = True
        else:
            self.target, self.arguments = slice[0], ArgumentList(slice[1])
            self.constructing_call = False

        if not self.arguments:
            self.arguments = ArgumentList()

    def describe(self):
        return 'target={}, args={}'.format(self.target, self.arguments)

    def replace_argument(self, idx, replacement):
        self.arguments[idx] = replacement

    def references(self):
        return self.target, self.arguments

    @classmethod
    def create_constructing_call(cls, target, arguments=None):
        return cls([LexicalClassInitialization(None), target, arguments if arguments is not None else ArgumentList()])

    @classmethod
    def create(cls, target, arguments=None):
        return cls([Access(target), arguments])

    def transpile(self, orphan=True):
        return f'{self.target.transpile()}({self.arguments.transpile()}){";" if orphan else ""}'

    def statics(self):
        yield from self.arguments.statics()

    def compile(self, context, captured=False):
        if self.target[0].implements(MethodCall):
            inner_target = self.target[0].compile(context, True)
            target = context.resolve(Access([inner_target.type, self.target[1]]))
        else:
            target = context.resolve(self.target)

            if not target.static and not self.constructing_call:
                context.push_ref(context.resolve(self.target[0]))

        for arg in self.arguments:
            context.push_ref(arg)

        instruction = OpcodeCallInternal if target.convention is Symbol.INTERNAL else OpcodeCall
        context.append(instruction.type_reference(target))

        if not captured:
            context.append(OpcodePop())  # pop the return value, if the return value is not captured

        return target


class ReturnStatement(BaseNode):
    def __init__(self, slice):
        super().__init__(slice)
        self.value = slice[1] if len(slice) == 2 else None

    def transpile(self):
        if self.value:
            return 'return Thing(new this_type({}));'.format(self.value.transpile())
        else:
            return 'return NULL;'

    def compile(self, context):
        context.push_ref(self.value)
        context.append(OpcodeReturn())
