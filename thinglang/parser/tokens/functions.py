from thinglang.lexer.symbols.base import  LexicalAccess, LexicalIdentifier
from thinglang.lexer.symbols.functions import LexicalClassInitialization
from thinglang.parser.tokens import BaseToken, DefinitionPairToken
from thinglang.parser.tokens.collections import ListInitializationPartial, ListInitialization
from thinglang.utils.type_descriptors import ValueType


class Access(BaseToken):
    def __init__(self, slice):
        super(Access, self).__init__(slice)
        self.target = [x for x in slice if not isinstance(x, LexicalAccess)]

    def evaluate(self, resolver):
        return resolver.resolve(self)

    def describe(self):
        return '.'.join(str(x) for x in self.target)

    def __getitem__(self, item):
        return self.target[item]


class ArgumentListPartial(ListInitializationPartial):
    pass


class ArgumentListDecelerationPartial(ArgumentListPartial):
    pass


class ArgumentList(ListInitialization):
    pass


class MethodCall(BaseToken, ValueType):
    def __init__(self, slice):
        super(MethodCall, self).__init__(slice)
        self.value = self

        if isinstance(slice[0], LexicalClassInitialization):
            self.target = Access([slice[1], LexicalIdentifier.constructor().contextify(slice[0])])
            self.arguments = slice[2]
            self.constructing_call = True
        else:
            self.target, self.arguments = slice
            self.constructing_call = False


        if not self.arguments:
            self.arguments = ArgumentList()

    def describe(self):
        return 'target={}, args={}'.format(self.target, self.arguments)

    def replace(self, original, replacement):
        self.arguments.replace(original, replacement)


class ReturnStatement(DefinitionPairToken):
    def __init__(self, slice):
        super().__init__(slice)
        self.value = slice[1]
