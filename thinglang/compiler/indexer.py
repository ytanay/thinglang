import collections
from collections import OrderedDict

from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.blocks.iteration_loop import IterationLoop
from thinglang.parser.blocks.try_block import TryBlock
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.definitions.thing_definition import ThingDefinition
from thinglang.parser.nodes.root_node import RootNode
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.utils.tree_utils import TreeTraversal, inspects

LocalMember = collections.namedtuple('LocalMember', ['type', 'index'])


class Indexer(TreeTraversal):
    """
    The indexer scans the AST for local variable declarations and allocates a slot for them in their respective
    method definitions's locals.

    This information is used during linking and reference resolution
    """

    def __init__(self, ast: RootNode):
        super(Indexer, self).__init__(ast)
        self.context = None

    def run(self):
        super().run()
        if self.context:
            self.context.flush()

    @inspects(MethodDefinition)
    def set_method_context(self, node: MethodDefinition):
        if self.context:
            self.context.flush()

        self.context = IndexerContext(node, self.current_thing)

    @inspects(AssignmentOperation)
    def index_local_variable(self, node: AssignmentOperation):
        if node.intent == node.DECELERATION:
            self.context.append(node.name, node.name.type)

    @inspects(IterationLoop)
    def index_iteration_loop(self, node: IterationLoop):
        self.context.append(*node.iterator_container_name)
        self.context.append(node.target, node.target_type)

    @inspects(TryBlock)
    def index_handle_block(self, node: TryBlock):
        for handler in node.handlers:
            if handler.exception_name is not None:
                self.context.append(handler.exception_name, handler.exception_type)


class IndexerContext(object):
    """
    An IndexerContext object is created for every method definition, and describes the slot ordering of the
    method's stack frame locals.

    When flushed, it copies the local descriptions into the appropriate method.
    """

    def __init__(self, method: MethodDefinition, thing: ThingDefinition):
        super(IndexerContext, self).__init__()

        self.current_method = method
        self.locals = OrderedDict({Identifier.self(): LocalMember(thing.name, 0)})
        for arg in method.arguments:
            self.locals[arg] = LocalMember(arg.type, len(self.locals))

    def flush(self):
        self.current_method.update_locals(self.locals)

    def append(self, name: Identifier, type: Identifier):
        if name in self.locals:  # TODO: this should be resolved within scoping rules
            return
        self.locals[name] = LocalMember(type, len(self.locals))

