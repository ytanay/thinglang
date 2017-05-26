import itertools

from thinglang.compiler.allocation import LinearMemoryAllocationLayout
from thinglang.compiler.references import ResolvedReference
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import ThingDefinition, MethodDefinition
from thinglang.parser.symbols.functions import MethodCall
from thinglang.utils.tree_utils import TreeTraversal, inspects


class IndexerContext(object):
    def __init__(self):
        self.instance_members, self.locals, self.current_method, self.current_thing = None, None, None, None
        self.method_index = 0
        self.things = []

    def over(self, thing_definition):
        self.current_thing = thing_definition
        self.things.append(thing_definition)
        self.instance_members = {
            member.name: (idx, member) for idx, member in enumerate(thing_definition.members())
        }

    def set_last_frame_size(self, size):
        if self.current_method:
            self.current_method.frame_size = size

    def set_method(self, node):
        self.current_method = node
        node.index = self.method_index
        self.method_index += 1


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
        self.context = IndexerContext()
        self.locals = None

    def run(self):
        super(Indexer, self).run()
        self.context.set_last_frame_size(self.locals.next_index)

    @inspects(ThingDefinition)
    def set_thing_context(self, node: ThingDefinition) -> None:
        self.context.over(node)

    @inspects(MethodDefinition)
    def set_method_context(self, node: MethodDefinition) -> None:
        if self.locals:
            self.context.set_last_frame_size(self.locals.next_index)

        self.context.set_method(node)
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
        print(node)
        node.arguments = [
            arg if arg.STATIC else ResolvedReference(self.locals.get(arg)) for arg in node.arguments
        ]

        if node.target[0].is_self():
            target = self.context.current_thing
            for x in node.target[1:]:
                target = target[x]
            node.resolved_target = ResolvedReference(target.index)

        print(node, node.arguments)

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