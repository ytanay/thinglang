from thinglang.compiler import OPCODES, BytecodeSymbols
from thinglang.foundation import templates
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalDeclarationConstructor
from thinglang.parser.symbols import DefinitionPairSymbol, BaseSymbol
from thinglang.parser.symbols.base import InlineString
from thinglang.parser.symbols.functions import ArgumentList, ReturnStatement


class ThingDefinition(DefinitionPairSymbol):
    SERIALIZATION = '<II'

    def __contains__(self, item):
        return any(child.name == item for child in self.children)

    def __getitem__(self, item):
        return [child for child in self.children if child.name == item][0]

    def describe(self):
        return self.name

    def transpile(self):
        name = '{}Instance'.format(self.name.transpile().capitalize())
        constructor = '\t{}({}) : val(val), ThingInstance() {{}}'.format(
            name,
            ', '.join('{} {}'.format(x.type.transpile(), x.name.transpile()) for x in self.members())
        )

        return '\n'.join([
            'class {};'.format(name),
            'typedef {} this_type;'.format(name),
            'class {} : public ThingInstance {{\npublic:\n{}\n{}\n{}\n{}\n}};'.format(
                name,
                constructor,
                templates.FOUNDATION_VIRTUALS.format(first_member=self.members()[0].name.transpile()),
                '\tstatic const std::vector<InternalMethod> methods;',
                self.transpile_children(indent=1))
        ])

    def members(self):
        return [x for x in self.children if x.implements(MemberDefinition)]

    def methods(self):
        return [x for x in self.children if x.implements(MethodDefinition)]

    def serialization(self):
        return len(self.members()), len(self.methods())

    def finalize(self):
        first_method = self.methods()[0]
        if not first_method.is_constructor:
            print('Creating default constructor!')
            index = self.children.index(first_method)
            self.children.insert(index, MethodDefinition([LexicalDeclarationConstructor, None]))


class MethodDefinition(BaseSymbol):
    SERIALIZATION = '<II'

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
        self.frame_size = None
        self.index = None

    def is_constructor(self):
        return self.name == LexicalIdentifier.constructor()

    def describe(self):
        return '{}, args={}'.format(self.name, self.arguments)

    def transpile(self):
        return 'static {}{}({}) {{\n{}\n{}\n\t}}'.format(
            self.return_type.transpile() + ' ' if self.return_type else 'void ' if not self.is_constructor() else '',
            (self.parent.name if self.is_constructor() else self.name).transpile(),
            '',  # Pop directly from stack, otherwise: self.arguments.transpile(definition=True),
            self.arguments.transpile(pops=True),
            self.transpile_children(2))

    def serialization(self):
        return self.frame_size, len(self.arguments)

    def set_type(self, type):
        if not self.return_type:
            self.return_type = type
        elif type is not self.return_type:
          return # TODO: reenable
          raise Exception('Multiple return types {}, {}'.format(type, self.return_type))

    def compile(self, context):
        context.method_start()
        super(MethodDefinition, self).compile(context)
        if not self.is_constructor() and not self.children[-1].implements(ReturnStatement):
            context.append(BytecodeSymbols.push_null())

        context.method_end()


class MemberDefinition(BaseSymbol):
    def __init__(self, slice):
        super(MemberDefinition, self).__init__(slice)

        _, self.type, self.name = slice

        if self.type.implements(InlineString):
            self.type = LexicalIdentifier(self.type.value)

    def describe(self):
        return 'has {} {}'.format(self.type, self.name)

    def transpile(self):
        return '{} {};'.format(self.type.transpile(), self.name.transpile())