from thinglang.parser.tokens import DefinitionPairToken
from thinglang.parser.tokens.functions import ArgumentList


class ThingDefinition(DefinitionPairToken):
    pass


class MethodDefinition(DefinitionPairToken):
    def __init__(self, slice):
        super(MethodDefinition, self).__init__(slice)

        if isinstance(slice[2], ArgumentList):
            self.arguments = slice[2].value
        else:
            self.arguments = []

    def describe(self):
        return '{}, args={}'.format(self.value, self.arguments)
