from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.blocks.conditional import Conditional
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.parser.statements.return_statement import ReturnStatement
from thinglang.parser.values.access import Access
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.inline_list import InlineList
from thinglang.parser.values.method_call import MethodCall
from thinglang.utils.tree_utils import TreeTraversal, inspects


class Simplifier(TreeTraversal):
    """
    The simplifier inspects certain language constructs and modifies them for simpler compilation into equivalent bytecode.
    """

    MULTI_ARG_CONSTRUCTS = MethodCall, InlineList

    @inspects((AssignmentOperation, ReturnStatement, Conditional, Loop))
    def simplify_assignment_operation(self, node: AssignmentOperation):
        """
        Checks the value of an assignment operation for values requiring simplification.
        Simplifies the value if needed.
        """
        if isinstance(node, ReturnStatement) and not node.value:
            return

        if isinstance(node.value, BinaryOperation):
            node.value = self.convert_arithmetic_operations(node.value)

        if isinstance(node.value, Simplifier.MULTI_ARG_CONSTRUCTS):
            self.simplify_multi_arg_constructs(node.value)

    @inspects(MULTI_ARG_CONSTRUCTS)
    def simplify_multi_arg_constructs(self, node: MethodCall):
        """
        Inspects a method call or inline list's arguments for values requiring simplification.
        Simplifies each argument in turn.
        """
        for idx, arg in enumerate(node.arguments):
            if isinstance(arg, BinaryOperation):
                node.replace_argument(idx, self.convert_arithmetic_operations(arg))
            elif isinstance(arg, Simplifier.MULTI_ARG_CONSTRUCTS):
                self.simplify_multi_arg_constructs(arg)

    def convert_arithmetic_operations(self, node: BinaryOperation) -> MethodCall:
        """
        Converts an arithmetic (binary) operation into a method call on the relevant type, recursively.
        """
        lhs, rhs = node.lhs, node.rhs

        if isinstance(lhs, BinaryOperation):
            lhs = self.convert_arithmetic_operations(lhs)
        elif isinstance(lhs, Simplifier.MULTI_ARG_CONSTRUCTS):
            self.simplify_multi_arg_constructs(lhs)

        if isinstance(rhs, BinaryOperation):
            rhs = self.convert_arithmetic_operations(rhs)
        elif isinstance(rhs, Simplifier.MULTI_ARG_CONSTRUCTS):
            self.simplify_multi_arg_constructs(rhs)

        if isinstance(lhs, Access):
            return MethodCall(lhs.append(Identifier(node.operator.transpile())), ArgumentList([rhs]))
        else:
            return MethodCall(Access([lhs, Identifier(node.operator.transpile())]), ArgumentList([rhs]))
