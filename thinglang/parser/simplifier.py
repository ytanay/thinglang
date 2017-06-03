from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import Transient
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.functions import MethodCall, Access, ArgumentList
from thinglang.parser.symbols.logic import IterativeLoop, Loop
from thinglang.parser.symbols.types import CastOperation
from thinglang.utils.tree_utils import TreeTraversal, inspects
from thinglang.utils.union_types import POTENTIALLY_OBTAINABLE


class Simplifier(TreeTraversal):

    @inspects(IterativeLoop)
    def unwrap_iterative_loops(self, node):
        generator_id, generator_declaration, generator_assignment = self.create_transient(node.generator, node, LexicalIdentifier('Range'))
        initial_assignment = AssignmentOperation.create(node.name, MethodCall.create([generator_id, 'next']), LexicalIdentifier('number')).set_context(node.parent)
        iterative_assignment = AssignmentOperation.create(node.name, MethodCall.create([generator_id, 'next']))

        condition, condition_declaration, condition_assignment = self.create_transient(MethodCall.create([generator_id, 'has_next']), node, LexicalIdentifier('boolean'))

        node.insert_before(generator_declaration)
        node.insert_before(initial_assignment)
        node.insert_before(condition_declaration)

        node.children.append(iterative_assignment)
        node.children.append(condition_assignment)

        loop = Loop([None, condition]).contextify(node.parent).populate(node.children)

        node.insert_before(loop)
        node.remove()

    @inspects(predicate=lambda x: isinstance(getattr(x, 'value', None), POTENTIALLY_OBTAINABLE))
    def inspect_obtainable_operations(self, node):
        return self.unwrap_method_calls(node.value, node)

    def unwrap_method_calls(self, method_call, node, parent_call=None):
        if not isinstance(method_call, POTENTIALLY_OBTAINABLE):
            return

        for argument in method_call.arguments:
            if isinstance(argument, POTENTIALLY_OBTAINABLE):
                self.unwrap_method_calls(argument, node, parent_call=method_call)

        if parent_call is not None:
            id, declaration, assignment = self.create_transient(method_call, node)
            node.insert_before(declaration)
            parent_call.replace(method_call, id)

    @classmethod
    def is_compound(cls, node):
        if not node:
            return False
        return (isinstance(node, MethodCall) and any(isinstance(arg, MethodCall) for arg in node.arguments.value)) or \
               (isinstance(node, AssignmentOperation) and cls.is_compound(node.value))

    @staticmethod
    def create_transient(value, parent, type=None):
        local_id = Transient().set_context(parent.context)
        return local_id, AssignmentOperation([type, local_id, None, value]).contextify(parent.parent), AssignmentOperation([local_id, None, value]).contextify(parent.parent)

