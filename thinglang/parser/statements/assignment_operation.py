from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeAssignStatic, OpcodeAssignLocal, OpcodePopLocal, OpcodePopMember
from thinglang.lexer.operators.assignment import LexicalAssignment
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.constructs.cast_operation import CastOperation
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.access import Access
from thinglang.utils.type_descriptors import ValueType


class AssignmentOperation(BaseNode):
    """
    Represents all flavors of assignment operations, static-to-local, static-to-member, local-to-local, member-to-member, etc...
    """

    DECELERATION = object()  # This assignment declares a local variable, and assigns an initial value to it
    REASSIGNMENT = object()  # This assignment refers to an existing local variable or to a member variable

    def __init__(self, intent, name, value, type_name=None):
        super(AssignmentOperation, self).__init__([name, value, type_name])
        self.intent, self.name, self.value = intent, name, value

        if type_name is not None:
           self.name.type = type_name

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

    ASSIGNMENT_TARGET = Identifier, Access

    @staticmethod
    @ParserRule.mark
    def assignment_declaration(type_name: Identifier, name: Identifier, _: LexicalAssignment, value: ValueType):
        return AssignmentOperation(AssignmentOperation.DECELERATION, name, value, type_name)

    @staticmethod
    @ParserRule.mark
    def assignment_reassignment(name: ASSIGNMENT_TARGET, _: LexicalAssignment, value: ValueType):
        return AssignmentOperation(AssignmentOperation.REASSIGNMENT, name, value)
