from thinglang.common import ObtainableValue
from thinglang.lexer.lexical_tokens import LexicalIdentifier
from thinglang.parser.tokens import ReturnStatement, AssignmentOperation


class IntermediateContext(object):
    def __init__(self, context):
        self.context = context


def id_generator():
    while True:
        yield object()


def simplify(tree):
    ids = id_generator()
    interesting_children = list(tree.find(lambda x: isinstance(x, ReturnStatement) and isinstance(x.value, ObtainableValue)))

    for child in interesting_children:
        children = child.parent.children
        idx = children.index(child)
        local_id = LexicalIdentifier(next(ids)).contextify(child.context)
        children[idx:idx + 1] = [AssignmentOperation([IntermediateContext(child.context), local_id, None, child.value]), ReturnStatement([None, local_id])]

    return tree