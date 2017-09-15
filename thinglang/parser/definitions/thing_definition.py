from thinglang.compiler.context import CompilationContext
from thinglang.compiler.sentinels import SentinelThingDefinition
from thinglang.foundation import templates
from thinglang.parser.common.definition_pair import DefinitionPairNode
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition


class ThingDefinition(DefinitionPairNode):

    def describe(self):
        return self.name

    def compile(self, context: CompilationContext):
        context.append(SentinelThingDefinition(len(self.members), len(self.methods)), self.source_ref)
        super().compile(context)

    def transpile(self):
        type_cls_name, instance_cls_name = templates.get_names(self.name)
        print('\n\n\n', self.name, self.methods)
        return templates.FOUNDATION_TYPE.format(
            type_cls_name=type_cls_name, instance_cls_name=instance_cls_name,
            member_list=templates.format_member_list(self.members),
            method_list=templates.format_method_list(self.methods),
            members=self.transpile_children(indent=0, children_override=self.members),
            methods=self.transpile_children(indent=0, children_override=self.methods)
        )

    @property
    def members(self):
        return [x for x in self.children if x.implements(MemberDefinition)]

    @property
    def methods(self):
        return [x for x in self.children if x.implements(MethodDefinition)]
