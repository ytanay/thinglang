from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes import Transient
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.base import AssignmentOperation
from thinglang.parser.nodes.functions import MethodCall, Access, ReturnStatement
from thinglang.parser.nodes.logic import Conditional, Loop
from thinglang.utils.tree_utils import TreeTraversal, inspects



class Simplifier(TreeTraversal):

    @inspects(Access)
    def unwrap_reference_chains(self, node: Access):
        """
        Converts compound reference chains into a series of mutating assignments.

        For example, the expression
            t0 = a.b.c.d
        Will be converted into
            t0 = a.b
            t0 = t0.c
            t0 = t0.d
        """

        if len(node) == 2:
            return

        transient_id, transient_declaration, transient_assignment = self.create_transient(node.partial(0), node)
        node.insert_before(transient_declaration)
        for target in node.target[2:]:
            node.insert_before(self.create_assignment(transient_id, Access([transient_id, target]), node))
        node.remove()

    @inspects((AssignmentOperation, ReturnStatement, Conditional, Loop))
    def simplify_assignment_operation(self, node: AssignmentOperation):
        if node.value.implements(ArithmeticOperation):
            node.value = self.convert_arithmetic_operations(node.value)

    @inspects(MethodCall)
    def simply_method_call(self, node: MethodCall):
        for idx, arg in enumerate(node.arguments):
            if arg.implements(ArithmeticOperation):
                node.replace_argument(idx, self.convert_arithmetic_operations(arg))
            elif arg.implements(MethodCall):
                self.simply_method_call(arg)

    def convert_arithmetic_operations(self, node: ArithmeticOperation):
        lhs, rhs = node.arguments
        if lhs.implements(ArithmeticOperation):
            lhs = self.convert_arithmetic_operations(lhs)
        elif lhs.implements(MethodCall):
            self.simply_method_call(lhs)
        if rhs.implements(ArithmeticOperation):
            rhs = self.convert_arithmetic_operations(rhs)
        elif rhs.implements(MethodCall):
            self.simply_method_call(rhs)
        return MethodCall.create([lhs, LexicalIdentifier(node.operator.transpile())], [rhs])

    @staticmethod
    def create_transient(value, parent, type=None):
        local_id = Transient().set_context(parent.context)
        return local_id, AssignmentOperation([type, local_id, None, value]).contextify(parent.parent), AssignmentOperation([local_id, None, value]).contextify(parent.parent)

    @staticmethod
    def create_assignment(local_id, value, parent):
        return AssignmentOperation([local_id, None, value]).contextify(parent.parent)
