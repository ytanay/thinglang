from thinglang.common import ObtainableValue
from thinglang.lexer.symbols.base import LexicalIdentifier
from thinglang.parser.tokens.base import AssignmentOperation
from thinglang.parser.tokens.functions import MethodCall, ReturnStatement


class Transient(object):
    def __init__(self, idx):
        self.idx = idx

    def __str__(self):
        return 'Transient({})'.format(self.idx)


def id_generator():
    counter = 0
    while True:
        yield Transient(counter)
        counter += 1

ids = id_generator()

def is_compound(node):
    if not node:
        return False
    return (isinstance(node, MethodCall) and any(isinstance(arg, MethodCall) for arg in node.arguments.value)) or \
           (isinstance(node, AssignmentOperation) and is_compound(node.value))


def create_transient(value, parent):
    local_id = LexicalIdentifier(next(ids))
    return local_id, AssignmentOperation([None, local_id, None, value]).contextify(parent.parent)


