from thinglang.compiler.allocation import LinearMemoryAllocationLayout
from thinglang.compiler.references import ResolvedReference
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import ThingDefinition, MethodDefinition
from thinglang.parser.symbols.functions import MethodCall
from thinglang.utils.tree_utils import TreeTraversal, inspects


class Collator(TreeTraversal):

    def __init__(self, ast):
        super(Collator, self).__init__(ast)
        self.thing_index = itertools.count(0)
        self.method_index = None

    @inspects(ThingDefinition)
    def set_thing_context(self, node: ThingDefinition) -> None:
        node.index = next(self.thing_index)
        node.finalize()
        self.method_index = itertools.count(0)

    @inspects(MethodDefinition)
    def set_method_context(self, node: MethodDefinition) -> None:
        node.index = next(self.method_index)


class Indexer(TreeTraversal):

    def __init__(self, ast):
        super().__init__(ast)
        self.instance_members, self.locals, self.current_method = None, None, None

    def run(self):
        super(Indexer, self).run()
        self.current_method.frame_size = self.locals.next_index

    @inspects(ThingDefinition)
    def set_thing_context(self, node: ThingDefinition) -> None:
        self.instance_members = {
            member.name: (idx, member) for idx, member in enumerate(node.members())
        }

    @inspects(MethodDefinition)
    def set_method_context(self, node: MethodDefinition) -> None:
        if self.current_method:
            self.current_method.frame_size = self.locals.next_index

        self.current_method = node
        self.locals = LinearMemoryAllocationLayout({
            argument: idx for idx, argument in enumerate(node.arguments)
        })

    @inspects(AssignmentOperation)
    def process_assignment_operation(self, node: AssignmentOperation) -> None:
        if node.intent is AssignmentOperation.DECELERATION:
            self.process_declaration(node)
        elif node.intent is AssignmentOperation.REASSIGNMENT:
            self.process_assignment(node)

    @inspects(MethodCall)
    def inspect_method_call(self, node: MethodCall) -> None:
        """
        The reference indexing for method calls involves 2 separate processes - resolving the method target,
        and resolving each and every argument
        """
        node.arguments = [
            arg if arg.STATIC else ResolvedReference(self.locals.get(arg)) for arg in node.arguments
        ]

    def process_declaration(self, node):
        if node in self.locals:
            raise Exception('Duplicate decleration')
        else:
            print('Setting a local variable')
            node.target = self.locals.add(node.name)

    def process_assignment(self, node: AssignmentOperation):
        if node.name.implements(LexicalIdentifier):
            node.target = self.locals.get(node.name)
            print('For {}, idx is {}'.format(node.name, self.locals.get(node.name)))
        else:
            raise Exception('cannot resolve references yet!')