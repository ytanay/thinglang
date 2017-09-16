from thinglang.compiler.context import CompilationContext
from thinglang.foundation import templates
from thinglang.parser.blocks.common import ElseBranchInterface
from thinglang.parser.nodes.base_node import BaseNode


class UnconditionalElse(BaseNode, ElseBranchInterface):
    def compile(self, context: CompilationContext):
        super(UnconditionalElse, self).compile(context)
        context.update_conditional_jumps()

    def transpile(self):
        return templates.ELSE_CLAUSE.format(body=self.transpile_children(indent=3))