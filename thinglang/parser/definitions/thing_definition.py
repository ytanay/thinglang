from thinglang.compiler.context import CompilationContext
from thinglang.compiler.sentinels import SentinelThingDefinition
from thinglang.foundation import templates
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.nodes import BaseNode


class ThingDefinition(BaseNode):

    def __init__(self, slice):
        super(ThingDefinition, self).__init__(slice)
        self.name = slice[1]

    def describe(self):
        return self.name

    def compile(self, context: CompilationContext):
        context.append(SentinelThingDefinition(len(self.members), len(self.methods)), self.source_ref)
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
        return [x for x in self.children if x.implements(MemberDefinition)]

    @property
    def methods(self):
        return [x for x in self.children if x.implements(MethodDefinition)]

    @property
    def names(self):
        return [x.name for x in self.members + self.methods]

    def format_member_list(self):
        return ', '.join('{} {}'.format(x.type.transpile(), x.name.transpile()) for x in self.members)

    def format_method_list(self):
        return ', '.join(['&{}'.format(x.name.transpile()) for x in self.methods])
