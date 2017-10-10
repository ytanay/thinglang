from thinglang.compiler.context import CompilationContext
from thinglang.compiler.sentinels import SentinelThingDefinition
from thinglang.foundation import templates
from thinglang.lexer.definitions.tags import LexicalInheritanceTag
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationThing
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule


class ThingDefinition(BaseNode):

    def __init__(self, name, extends=None):
        super(ThingDefinition, self).__init__([name, extends])
        self.name, self.extends = name, extends

    def describe(self):
        return self.name

    def compile(self, context: CompilationContext):
        context.append(SentinelThingDefinition(self.slots(context), len(self.methods)), self.source_ref, directly=True)
        super().compile(context)

    def transpile(self):
        type_cls_name, instance_cls_name = self.container_name

        return templates.FOUNDATION_TYPE_DEFINITION.format(
            type_cls_name=type_cls_name, instance_cls_name=instance_cls_name,
            member_list=self.format_member_list(),
            method_list=self.format_method_list(),
            constructors=templates.FOUNDATION_VALUE_CONSTRUCTOR.format(instance_cls_name=instance_cls_name, member_list=self.format_member_list()) if self.members else '',
            mixins=templates.FOUNDATION_MIXINS_DEFINITION.format(instance_cls_name=instance_cls_name) if self.members else '',
            members=self.transpile_children(indent=0, children_override=self.members),
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

    def format_member_list(self):
        return ', '.join('{} {}'.format(x.type.transpile(), x.name.transpile()) for x in self.members)

    def format_method_list(self):
        return ', '.join(['&{}'.format(x.name.transpile()) for x in self.methods])

    @staticmethod
    @ParserRule.mark
    def definition_with_extends(_1: LexicalDeclarationThing, name: Identifier, _2: LexicalInheritanceTag, extends: Identifier):
        return ThingDefinition(name, extends)

    @staticmethod
    @ParserRule.mark
    def simple_definition(_: LexicalDeclarationThing, name: Identifier):
        return ThingDefinition(name)
