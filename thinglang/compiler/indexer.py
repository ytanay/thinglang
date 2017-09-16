import collections
from collections import OrderedDict

from thinglang.lexer.values.identifier import Identifier
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
            self.context.append(node)


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

    def append(self, node: AssignmentOperation):
        self.locals[node.name] = LocalMember(node.name.type, len(self.locals))

