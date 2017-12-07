from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.context import CompilationContext
from thinglang.foundation import templates
from thinglang.lexer.definitions.tags import LexicalInheritanceTag
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationThing
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule


class ThingDefinition(BaseNode):
    """
    Defines a thing, also known as a class
    """

    def __init__(self, name, extends=None, generics=None):
        super(ThingDefinition, self).__init__([name, extends, generics])
        self.name, self.extends, self.generics = name, extends, generics

    def __repr__(self):
        return f'thing {self.name}'

    def compile(self, context: CompilationContext):
        symbol_map = context.symbols[self.name]
        for method in self.methods:
            buffer = CompilationBuffer(context.symbols, method.locals)
            method.compile(buffer)
            context.add((symbol_map.index, symbol_map[method.name].index), method, buffer)

    def transpile(self):
        type_cls_name, instance_cls_name = self.container_name

        return templates.FOUNDATION_TYPE_DEFINITION.format(
            type_cls_name=type_cls_name, instance_cls_name=instance_cls_name,
            mixins=templates.FOUNDATION_MIXINS_DEFINITION.format(instance_cls_name=instance_cls_name, first_member=self.members[0].name.transpile()) if self.members else '',
            methods=self.transpile_children(indent=0, children_override=self.methods)
        )

    def finalize(self):
        super().finalize()

        if Identifier.constructor() not in self.names:  # Add implicit constructor
            self.children.insert(0, MethodDefinition.empty_constructor(self))

    @property
    def members(self):
        return [x for x in self.children if isinstance(x, MemberDefinition)]

    @property
    def methods(self):
        return [x for x in self.children if isinstance(x, MethodDefinition)]

    @property
    def names(self):
        return [x.name for x in self.members + self.methods]

    def slots(self, context):
        return sum(len(container.members) for container in context.symbols.inheritance(self))

    def format_method_list(self):
        return ', '.join(['&{}'.format(x.name.transpile()) for x in self.methods])

    @staticmethod
    @ParserRule.mark
    def base_definition(_: LexicalDeclarationThing, name: Identifier):
        return ThingDefinition(name)

    @staticmethod
    @ParserRule.mark
    def define_generic(thing: 'ThingDefinition', generics: 'TypeVector'):
        thing.generics = generics
        return thing

    @staticmethod
    @ParserRule.mark
    def define_inheritance(thing: 'ThingDefinition', _: LexicalInheritanceTag, extends: Identifier):
        thing.extends = extends
        return thing


