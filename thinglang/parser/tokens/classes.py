from thinglang.lexer.symbols import LexicalGroupEnd
from thinglang.lexer.symbols.base import LexicalIdentifier
from thinglang.lexer.symbols.functions import LexicalDeclarationConstructor
from thinglang.parser.tokens import DefinitionPairToken, BaseToken
from thinglang.parser.tokens.functions import ArgumentList


class ThingDefinition(DefinitionPairToken):

    def __contains__(self, item):
        return any(child.value == item for child in self.children)

    def __getitem__(self, item):
        return [child for child in self.children if child.value == item][0]

    def describe(self):
        return self.name

class MethodDefinition(BaseToken):
    def __init__(self, slice):
        super(MethodDefinition, self).__init__(slice)

        if isinstance(slice[0], LexicalDeclarationConstructor):
            self.name = LexicalIdentifier.constructor()
            argument_list = slice[1]
        else:
            self.name = slice[1]
            argument_list = slice[2]

        if isinstance(argument_list, ArgumentList):
            self.arguments = argument_list
        else:
            self.arguments = ArgumentList()

    def describe(self):
        return '{}, args={}'.format(self.name, self.arguments)


class MemberDefinition(BaseToken):
    def __init__(self, slice):
        super(MemberDefinition, self).__init__(slice)

        _, self.type, self.name = slice

    def describe(self):
        return 'has {} {}'.format(self.type, self.name)
