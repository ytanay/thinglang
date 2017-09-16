from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeAssignStatic, OpcodeAssignLocal, OpcodePopLocal, OpcodePopMember
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.values.access import Access
from thinglang.parser.values.method_call import MethodCall


class AssignmentOperation(BaseNode):
    """
    Represents all flavors of assignment operations, static-to-local, static-to-member, local-to-local, member-to-member, etc...
    """

    DECELERATION = object()  # This assignment declares a local variable, and assigns an initial value to it
    REASSIGNMENT = object()  # This assignment refers to an existing local variable or to a member variable

    def __init__(self, slice):
        super(AssignmentOperation, self).__init__(slice)

        if len(slice) == 4:
            _1, self.name, _2, self.value = slice
            self.name.type = slice[0]
            self.intent = self.DECELERATION
        else:
            self.name, _, self.value = slice
            self.intent = self.REASSIGNMENT

    def describe(self):
        return '{} = {}'.format(self.name, self.value)

    def compile(self, context: CompilationContext):

        is_local = self.name.implements(LexicalIdentifier)

        if is_local:
            target = context.resolve(self.name)

            if self.value.STATIC:
                ref = context.append_static(self.value.serialize())
                return context.append(OpcodeAssignStatic.from_reference(target, ref), self.source_ref)
            elif self.value.implements(LexicalIdentifier):
                ref = context.resolve(self.value)
                return context.append(OpcodeAssignLocal.from_references(target, ref), self.source_ref)

        if self.value.implements(MethodCall):
            self.value.compile(context)
        else:
            self.value.compile(context)

        target = self.name
        if target.implements(LexicalIdentifier):
            target = context.resolve(target)
            context.append(OpcodePopLocal.from_reference(target), self.source_ref)
        elif target.implements(Access):
            if target.extensions:
                target.compile(context, pop_last=True)
            else:
                context.append(OpcodePopMember.from_reference(context.resolve(target)), self.source_ref)

        else:
            raise Exception('Cannot pull up {}'.format(target))
