from thinglang.common import ObtainableValue
from thinglang.lexer.lexical_tokens import LexicalIdentifier
from thinglang.parser.tokens import ReturnStatement, AssignmentOperation, MethodCall


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


def simplify(tree):
    while unwrap_method_calls(tree):
        pass

    while unwrap_returns(tree):
        pass

    return tree

def unwrap_returns(tree):
    had_change = False

    for child in set(tree.find(lambda x: isinstance(x, ReturnStatement) and isinstance(x.value, ObtainableValue))):
        siblings = child.parent.children
        idx = siblings.index(child)
        local_id = LexicalIdentifier(next(ids)).contextify(child.context)
        siblings[idx:idx + 1] = [AssignmentOperation([None, local_id, None, child.value]), ReturnStatement([None, local_id])]
        had_change = True

    return had_change

def unwrap_method_calls(tree):
    relevant = list(tree.find(is_compound))

    if not relevant:
        return False

    child = relevant[0]

    parent, siblings = child.parent, child.parent.children
    idx = siblings.index(child)
    new_args = []

    if isinstance(child, AssignmentOperation):
        child = child.value

    for arg in child.arguments.value:
        if isinstance(arg, ObtainableValue):
            local_id = LexicalIdentifier(next(ids)).contextify(child.context)
            op = AssignmentOperation([None, local_id, None, arg])
            op.parent = parent
            siblings.insert(idx, op)
            new_args.append(local_id)
        else:
            new_args.append(arg)
    print('Against {}, {} -> {}'.format(child.target, child.arguments, new_args))
    assert len(child.arguments.value) == len(new_args)
    child.arguments.value = new_args

    return True
