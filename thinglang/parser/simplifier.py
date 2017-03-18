from thinglang.lexer.symbols.base import LexicalIdentifier
from thinglang.parser.tokens import Transient
from thinglang.parser.tokens.arithmetic import ArithmeticOperation
from thinglang.parser.tokens.base import AssignmentOperation
from thinglang.parser.tokens.functions import MethodCall, ReturnStatement


def simplify(tree):
    while unwrap_returns(tree):
        pass

    for method_call in tree.find(lambda x: isinstance(getattr(x, 'value', None), (MethodCall, ArithmeticOperation))):
        reduce_method_calls(method_call.value, method_call)

    return tree


def unwrap_returns(tree):
    had_change = False

    for child in set(tree.find(lambda x: isinstance(x, ReturnStatement) and isinstance(x.value, (MethodCall, ArithmeticOperation)))):
        id, assignment = create_transient(child.value, child)
        siblings = child.parent.children
        idx = siblings.index(child)

        siblings[idx:idx + 1] = [assignment, ReturnStatement([None, id]).contextify(child.parent)]
        had_change = True

    return had_change


def reduce_method_calls(method_call, node, parent_call=None):
    if not isinstance(method_call, (MethodCall, ArithmeticOperation)):
        return
    for argument in method_call.arguments:
        if isinstance(argument, MethodCall):
            reduce_method_calls(argument, node, parent_call=method_call)
        if isinstance(argument, ArithmeticOperation):
            for x in argument.arguments:
                reduce_method_calls(x, node, parent_call=argument)

    if parent_call is not None:
        id, assignment = create_transient(method_call, node)
        node.insert_before(assignment)
        parent_call.replace_argument(method_call, id)


def is_compound(node):
    if not node:
        return False
    return (isinstance(node, MethodCall) and any(isinstance(arg, MethodCall) for arg in node.arguments.value)) or \
           (isinstance(node, AssignmentOperation) and is_compound(node.value))


def create_transient(value, parent):
    local_id = LexicalIdentifier(Transient()).contextify(parent.context)
    return local_id, AssignmentOperation([None, local_id, None, value]).contextify(parent.parent)


