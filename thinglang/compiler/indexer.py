import collections
from collections import OrderedDict

from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.base import AssignmentOperation
from thinglang.parser.nodes.classes import MethodDefinition
from thinglang.utils.tree_utils import TreeTraversal, inspects


LocalMember = collections.namedtuple('LocalMember', ['type', 'index'])


class Indexer(TreeTraversal):

    def __init__(self, ast):
        super(Indexer, self).__init__(ast)
        self.context: IndexerContext = None

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

    def __init__(self, method, thing):
        super(IndexerContext, self).__init__()

        self.current_method: MethodDefinition = method
        self.locals = OrderedDict({LexicalIdentifier.self(): LocalMember(thing.name, 0)})
        for arg in method.arguments:
            self.locals[arg] = LocalMember(arg.type, len(self.locals))

    def flush(self):
        self.current_method.update_locals(self.locals)

    def append(self, node: AssignmentOperation):
        self.locals[node.name] = LocalMember(node.name.type, len(self.locals))

