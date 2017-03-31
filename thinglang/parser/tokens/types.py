from thinglang.lexer.symbols.base import LexicalIdentifier
from thinglang.parser.tokens import BaseToken
from thinglang.parser.tokens.collections import ListInitializationPartial, ListInitialization
from thinglang.utils.type_descriptors import ValueType, ReplaceableArguments


class ArrayInitializationPartial(ListInitializationPartial):
    pass


class ArrayInitialization(ListInitialization, ValueType):
    pass


class CastOperation(BaseToken, ValueType, ReplaceableArguments):

    CASTERS = {
        LexicalIdentifier("number"): lambda x: int(x)
    }

    def __init__(self, slice):
        super(CastOperation, self).__init__(slice)
        self.arguments = [slice[0]]
        self.caster = self.CASTERS[slice[2]]

    def evaluate(self, resolver):
        return self.caster(self.arguments[0].evaluate(resolver))