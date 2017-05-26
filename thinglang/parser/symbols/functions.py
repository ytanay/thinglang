from thinglang.compiler import BytecodeSymbols
from thinglang.compiler.indexer import ResolvedReference
from thinglang.lexer.tokens.base import LexicalAccess, LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalClassInitialization
from thinglang.parser.symbols import BaseSymbol, DefinitionPairSymbol
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
        if self.target[0].is_self():
            return self.target[0].transpile() + '->' + '.'.join(x.transpile() for x in self.target[1:])

        return '.'.join(x.transpile() for x in self.target)


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

    def compile(self, context):
        for arg in self.arguments:
            if isinstance(arg, ResolvedReference):
                context.append(BytecodeSymbols.push(arg.index))
            elif arg.STATIC:
                id = context.append_static(arg.serialize())
                context.append(BytecodeSymbols.push_static(id))
            else:
                raise Exception('Strange argument type {}'.format(arg))

        if self.target[0].is_self():
            context.append(BytecodeSymbols.call_method(self.resolved_target.index))
        else:
            context.append(BytecodeSymbols.call_internal(0, 0))


class ReturnStatement(DefinitionPairSymbol):
    def __init__(self, slice):
        super().__init__(slice)
        self.value = slice[1]

    def transpile(self):
        return 'return {};'.format(self.value.transpile())
