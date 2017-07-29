from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes import Transient
from thinglang.parser.nodes.base import AssignmentOperation
from thinglang.parser.nodes.functions import MethodCall, Access, ReturnStatement
from thinglang.parser.nodes.logic import IterativeLoop, Loop
from thinglang.utils.tree_utils import TreeTraversal, inspects
from thinglang.utils.union_types import POTENTIALLY_OBTAINABLE


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

    @inspects(IterativeLoop)
    def unwrap_iterative_loops(self, node: IterativeLoop):
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

    @inspects(ReturnStatement)
    def inspect_return_statement(self, node: ReturnStatement) -> None:
        if node.value and node.value.implements(POTENTIALLY_OBTAINABLE):
            id, declaration, assignment = self.create_transient(node.value, node)
            node.insert_before(declaration)
            node.value = id

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

    @staticmethod
    def create_assignment(local_id, value, parent):
        return AssignmentOperation([local_id, None, value]).contextify(parent.parent)
