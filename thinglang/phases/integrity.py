from thinglang.parser.blocks.common import ElseBranchInterface
from thinglang.parser.blocks.conditional import Conditional
from thinglang.parser.blocks.conditional_else import ConditionalElse
from thinglang.parser.blocks.handle_block import HandleBlock
from thinglang.parser.blocks.try_block import TryBlock
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.definitions.thing_definition import ThingDefinition
from thinglang.parser.errors import StructureError, CustomStructureError
from thinglang.parser.nodes.root_node import RootNode
from thinglang.utils.tree_utils import TreeTraversal, inspects


class StructuralIntegrity(TreeTraversal):
    """
    The StructuralIntegrity traversal verifies that every node's children are of appropriate types
    """

    def run(self):
        assert isinstance(self.ast, RootNode), 'Root of AST must be a RootNode'
        super().run()

    @inspects(RootNode)
    def inspect_root_node(self, node: RootNode):
        failing = self.verify(node, ThingDefinition)
        if failing:
            raise StructureError(node, failing, ThingDefinition)

    @inspects(ThingDefinition)
    def inspect_thing_definition(self, node: ThingDefinition):
        failing = self.verify(node, (MethodDefinition, MemberDefinition))
        if failing:
            raise StructureError(node, failing, (MethodDefinition, MemberDefinition))

    @inspects(MethodDefinition)
    def inspect_method_definition(self, node: MethodDefinition):
        failing = [child for child in node.children if isinstance(child, (ThingDefinition, MemberDefinition, MethodDefinition))]
        if failing:
            raise StructureError(node, failing, (ThingDefinition, MemberDefinition, MethodDefinition), True)

    @inspects(ConditionalElse)  # TODO: move this to collection in Conditional
    def inspect_conditional_else(self, node):
        if not isinstance(node.previous_sibling(), Conditional):  # TODO Broken, because the first conditional might also be a ConditionalElse
            raise CustomStructureError(node, 'A ConditionalElse must come after a conditional')

    @inspects(ElseBranchInterface)
    def inspect_else_branch(self, node):
        if not isinstance(node.previous_sibling(), (Conditional)):
            raise CustomStructureError(node, 'A {type(node).__name__} must come after a conditional')

    def verify(self, node, allowed_children):
        return [child for child in node.children if not isinstance(child, allowed_children)]