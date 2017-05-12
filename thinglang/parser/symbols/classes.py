from thinglang.lexer.tokens import LexicalGroupEnd
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalDeclarationConstructor
from thinglang.parser.symbols import DefinitionPairSymbol, BaseSymbol
from thinglang.parser.symbols.functions import ArgumentList


class ThingDefinition(DefinitionPairSymbol):

    def __contains__(self, item):
        return any(child.name == item for child in self.children)

    def __getitem__(self, item):
        return [child for child in self.children if child.name == item][0]

    def describe(self):
        return self.name

    def transpile(self):
        return 'class {} {{\npublic:\n{}\n}};'.format(self.name.value, self.transpile_children(indent=1))


class MethodDefinition(BaseSymbol):
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

        self.return_type = None

    def is_constructor(self):
        return self.name == LexicalIdentifier.constructor()

    def describe(self):
        return '{}, args={}'.format(self.name, self.arguments)

    def transpile(self):
        return '{}{}({}) {{\n{}\n\t}}'.format(self.return_type.transpile() + ' ' if self.return_type else 'void ' if not self.is_constructor() else '', (self.parent.name if self.is_constructor() else self.name).value, self.arguments.transpile(definition=True), self.transpile_children(2))

    def set_type(self, type):
        if not self.return_type:
            self.return_type = type
        elif type is not self.return_type:
          raise Exception('Multiple return types {}, {}'.format(type, self.return_type))

class MemberDefinition(BaseSymbol):
    def __init__(self, slice):
        super(MemberDefinition, self).__init__(slice)

        _, self.type, self.name = slice

    def describe(self):
        return 'has {} {}'.format(self.type, self.name)

    def transpile(self):
        return '{} {};'.format(self.type.transpile(), self.name.transpile())