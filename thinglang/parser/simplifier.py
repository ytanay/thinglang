from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.base import AssignmentOperation
from thinglang.parser.nodes.functions import MethodCall, ReturnStatement
from thinglang.parser.nodes.logic import Conditional, Loop
from thinglang.utils.tree_utils import TreeTraversal, inspects


class Simplifier(TreeTraversal):

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
