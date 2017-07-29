import collections

from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.base import AssignmentOperation
from thinglang.parser.nodes.classes import  MethodDefinition
from thinglang.utils.tree_utils import TreeTraversal, inspects


LocalMember = collections.namedtuple('LocalMember', ['name', 'type'])


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

        self.context = IndexerContext(node)

    @inspects(AssignmentOperation)
    def index_local_variable(self, node: AssignmentOperation):
        if node.intent == node.DECELERATION:
            self.context.append(node)


class IndexerContext(object):

    def __init__(self, method=None):
        super(IndexerContext, self).__init__()

        self.current_method: MethodDefinition = method
        self.locals = [LexicalIdentifier.self()]

    def flush(self):
        self.current_method.update_locals(self.locals)

    def append(self, node: AssignmentOperation):
        self.locals.append(LocalMember(node.name, node.name.type))

