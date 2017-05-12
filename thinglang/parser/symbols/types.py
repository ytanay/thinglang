from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import BaseSymbol
from thinglang.parser.symbols.collections import ListInitializationPartial, ListInitialization
from thinglang.utils.type_descriptors import ValueType, ReplaceableArguments


class ArrayInitializationPartial(ListInitializationPartial):
    pass


class ArrayInitialization(ListInitialization, ValueType):
    def transpile(self, definition=False):
        return '[{}]'.format(super(ArrayInitialization, self).transpile(definition=definition))


class CastOperation(BaseSymbol, ValueType, ReplaceableArguments):

    CASTERS = {
        LexicalIdentifier("number"): lambda x: int(x)
    }

    def __init__(self, slice):
        super(CastOperation, self).__init__(slice)
        self.arguments = [slice[0]]
        self.caster = self.CASTERS[slice[2]]

    def evaluate(self, resolver):
        return self.caster(self.arguments[0].evaluate(resolver))
