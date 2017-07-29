from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.parser.nodes import RootNode
from thinglang.parser.nodes.classes import MethodDefinition, ThingDefinition
from thinglang.parser.nodes.functions import MethodCall
from thinglang.utils.tree_utils import TreeTraversal, inspects


class Resolver(TreeTraversal):
    
    def __init__(self, ast: RootNode, symbols: SymbolMapper):
        super(Resolver, self).__init__(ast)

        self.symbols = symbols
        self.current_thing, self.current_method = None, None

    @inspects(ThingDefinition)
    def update_thing_context(self, node: ThingDefinition):
        self.current_thing = node

    @inspects(MethodDefinition)
    def update_method_context(self, node: MethodDefinition):
        self.current_method = node

    @inspects(MethodCall)
    def resolve_method_call(self, node: MethodCall):
        node.resolve(self.symbols.resolve(node.target))
