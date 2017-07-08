from thinglang.compiler import OPCODES, BytecodeSymbols
from thinglang.foundation import templates
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalDeclarationConstructor, LexicalDeclarationReturnType
from thinglang.parser.symbols import DefinitionPairSymbol, BaseSymbol
from thinglang.parser.symbols.base import InlineString
from thinglang.parser.symbols.functions import ArgumentList, ReturnStatement, ArgumentListPartial


class ThingDefinition(DefinitionPairSymbol):
    SERIALIZATION = '<II'

    def __contains__(self, item):
        return any(child.name == item for child in self.children)

    def __getitem__(self, item):
        return [child for child in self.children if child.name == item][0]

    def describe(self):
        return self.name

    def transpile(self):
        name = self.name.transpile().capitalize()
        type_name, instance_name = '{}Type'.format(name), '{}Instance'.format(name)
        constructor = '\t{}({}) : val(val) {{}};'.format(
            instance_name,
            ', '.join('{} {}'.format(x.type.transpile(), x.name.transpile()) for x in self.members())
        )

        return '\n'.join([
            '\nclass {} : public BaseThingInstance {{\npublic:\n{}\n{}\n{}\n\n{}\n}};'.format(
                instance_name,
                templates.DEFAULT_CONSTRUCTOR.format(instance_name),
                constructor,
                '''
    virtual std::string text() override {
        return to_string(val);
    }
                ''',
                self.transpile_children(indent=1, children_override=self.members())
            ),

            'typedef {} this_type;\n'.format(instance_name),
            'class {} : public ThingTypeInternal {{\npublic:\n{}\n{}\n{}\n}};'.format(
                type_name,
                '\t{}() : ThingTypeInternal({{{}}}) {{}};'.format(type_name, ', '.join(['&{}'.format(x.name.transpile()) for x in self.methods()])),
                templates.FOUNDATION_VIRTUALS.format(first_member=self.members()[0].name.transpile()),
                self.transpile_children(indent=1, children_override=self.methods()))
        ])

    def members(self):
        return [x for x in self.children if x.implements(MemberDefinition)]

    def methods(self):
        return [x for x in self.children if x.implements(MethodDefinition)]

    def serialization(self):
        return len(self.members()), len(self.methods())

    def finalize(self):
        methods = self.methods()
        if not methods or not methods[0].is_constructor:
            print('Creating default constructor!')
            index = self.children.index(methods[0]) if methods else 0
            self.children.insert(index, MethodDefinition([LexicalDeclarationConstructor, None]))


class MethodDefinition(BaseSymbol):
    SERIALIZATION = '<II'

    def __init__(self, slice):
        super(MethodDefinition, self).__init__(slice)

        self.arguments = None
        self.return_type = None
        self.frame_size = None
        self.index = None

        if isinstance(slice[0], LexicalDeclarationConstructor):
            self.name = LexicalIdentifier.constructor()
            self.arguments = slice[1]
        else:
            self.name = slice[1]

            if isinstance(slice[2], ArgumentList):
                self.arguments = slice[2]
            elif isinstance(slice[2], ArgumentListPartial):
                self.arguments = ArgumentList([slice[2]])

            elif isinstance(slice[2], LexicalDeclarationReturnType):
                self.return_type = slice[3]

            if len(slice) >= 4 and isinstance(slice[3], LexicalDeclarationReturnType):
                self.return_type = slice[4]

        if not isinstance(self.arguments, ArgumentList):
            self.arguments = ArgumentList()

    def is_constructor(self):
        return self.name == LexicalIdentifier.constructor()

    def describe(self):
        return '{}, args={}'.format(self.name, self.arguments)

    def transpile(self):
        return 'static {} {}({}) {{\n{}\n{}\n\t}}'.format(
            'Thing' if not self.is_constructor() else '',
            (self.parent.name if self.is_constructor() else self.name).transpile(),
            '',  # Pop directly from stack, otherwise: self.arguments.transpile(definition=True),
            self.arguments.transpile(pops=True),
            self.transpile_children(2, self.children + [ReturnStatement([])]))

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

    def type_id(self):
        return self.return_type


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