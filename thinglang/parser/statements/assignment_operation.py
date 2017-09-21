from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeAssignStatic, OpcodeAssignLocal, OpcodePopLocal, OpcodePopMember
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.constructs.cast_operation import CastOperation
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

        is_local = self.name.implements(Identifier)

        if is_local:
            target = context.resolve(self.name)

            if self.value.STATIC:
                ref = context.append_static(self.value.serialize())
                return context.append(OpcodeAssignStatic.from_reference(target, ref), self.source_ref)
            elif self.value.implements(Identifier):
                ref = context.resolve(self.value)
                return context.append(OpcodeAssignLocal.from_references(target, ref), self.source_ref)

        value_ref = self.value.compile(context)
        target = self.name

        cast_placeholder = context.current_index() + 1

        if target.implements(Identifier):
            target_ref = context.resolve(target)
            context.append(OpcodePopLocal.from_reference(target_ref), self.source_ref)
        elif target.implements(Access):
            if target.extensions:
                target_ref = target.compile(context, pop_last=True)
            else:
                target_ref = context.resolve(target)
                context.append(OpcodePopMember.from_reference(target_ref), self.source_ref)
        else:
            raise Exception('Cannot pull up {}'.format(target))

        if value_ref.type != target_ref.type:
            buffer = context.buffer()
            CastOperation.create(source=value_ref.type, destination=target_ref.type).deriving_from(self).compile(buffer)
            context.insert(cast_placeholder, buffer)
