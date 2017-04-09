from thinglang.parser.symbols import Transient
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.functions import MethodCall
from thinglang.parser.symbols.types import CastOperation
from thinglang.utils.tree_utils import TreeTraversal, inspects
from thinglang.utils.union_types import POTENTIALLY_OBTAINABLE


class Simplifier(TreeTraversal):

    @inspects(predicate=lambda x: isinstance(getattr(x, 'value', None), POTENTIALLY_OBTAINABLE))
    def inspect_obtainable_operations(self, node):
        return self.unwrap_method_calls(node.value, node)

    def unwrap_method_calls(self, method_call, node, parent_call=None):
        if not isinstance(method_call, POTENTIALLY_OBTAINABLE):
            return

        for argument in method_call.arguments:
            if isinstance(argument, (MethodCall, CastOperation)):
                self.unwrap_method_calls(argument, node, parent_call=method_call)
            if isinstance(argument, ArithmeticOperation):
                for x in argument.arguments:
                    self.unwrap_method_calls(x, node, parent_call=argument)

        if parent_call is not None:
            id, assignment = self.create_transient(method_call, node)
            node.insert_before(assignment)
            parent_call.replace(method_call, id)

    @classmethod
    def is_compound(cls, node):
        if not node:
            return False
        return (isinstance(node, MethodCall) and any(isinstance(arg, MethodCall) for arg in node.arguments.value)) or \
               (isinstance(node, AssignmentOperation) and cls.is_compound(node.value))

    @staticmethod
    def create_transient(value, parent, type=None):
        local_id = Transient().contextify(parent.context)
        return local_id, AssignmentOperation([type, local_id, None, value]).contextify(parent.parent)

