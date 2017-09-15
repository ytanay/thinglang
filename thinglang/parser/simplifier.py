from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.values.binary_operation import BinaryOperation
from thinglang.parser.nodes.statements.assignment_operation import AssignmentOperation
from thinglang.parser.nodes.blocks.conditional import Conditional
from thinglang.parser.nodes.blocks.loop import Loop
from thinglang.parser.nodes.values.method_call import MethodCall
from thinglang.parser.nodes.statements.return_statement import ReturnStatement
from thinglang.utils.tree_utils import TreeTraversal, inspects


class Simplifier(TreeTraversal):
    """
    The simplifier inspects certain language constructs and modifies them for simpler compilation into equivalent bytecode.
    """

    @inspects((AssignmentOperation, ReturnStatement, Conditional, Loop))
    def simplify_assignment_operation(self, node: AssignmentOperation):
        """
        Checks the value of an assignment operation for values requiring simplification.
        Simplifies the value if needed.
        """
        if node.value.implements(BinaryOperation):
            node.value = self.convert_arithmetic_operations(node.value)

    @inspects(MethodCall)
    def simply_method_call(self, node: MethodCall):
        """
        Inspects a method call's arguments for values requiring simplification.
        Simplifies each argument in turn.
        """
        for idx, arg in enumerate(node.arguments):
            if arg.implements(BinaryOperation):
                node.replace_argument(idx, self.convert_arithmetic_operations(arg))
            elif arg.implements(MethodCall):
                self.simply_method_call(arg)

    def convert_arithmetic_operations(self, node: BinaryOperation) -> MethodCall:
        """
        Converts an arithmetic (binary) operation into a method call on the relevant type, recursively.
        """
        lhs, rhs = node.arguments

        if lhs.implements(BinaryOperation):
            lhs = self.convert_arithmetic_operations(lhs)
        elif lhs.implements(MethodCall):
            self.simply_method_call(lhs)
        if rhs.implements(BinaryOperation):
            rhs = self.convert_arithmetic_operations(rhs)
        elif rhs.implements(MethodCall):
            self.simply_method_call(rhs)

        return MethodCall.create([lhs, LexicalIdentifier(node.operator.transpile())], [rhs])
