from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodeAssignStatic, OpcodeAssignLocal, OpcodePopLocal, OpcodePopMember
from thinglang.lexer.operators.assignment import LexicalAssignment
from thinglang.lexer.operators.binary import LexicalBinaryOperation
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.constructs.cast_operation import CastOperation
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.indexed_access import IndexedAccess
from thinglang.parser.values.named_access import NamedAccess
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
            assert self.name.type is None or self.name.type == type_name, f'Overriding {self.name.type} -> {type_name}'
            self.name.type = type_name

    def __repr__(self):
        return f'Assignment({self.name} = {self.value})'

    def compile(self, context: CompilationBuffer):
        if isinstance(self.name, IndexedAccess):  # Should validate types implicitly
            return self.name.assignment(self.value).compile(context)

        value_buffer, target_buffer = context.optional(), context.optional()
        value_ref = self.value.compile(value_buffer)
        target_ref = self.pull_up(self.name, target_buffer)

        if value_ref.type.untyped != target_ref.type.untyped:  # TODO: why is the test against untyped?
            CastOperation(self.value, target_ref.type).compile(context)
        elif self.optimized_assignment(context):
            return
        else:
            context.extend(value_buffer)

        context.extend(target_buffer)

    def optimized_assignment(self, context):
        if isinstance(self.name, Identifier):
            target = context.resolve(self.name)

            if self.value.STATIC:
                ref = context.append_static(self.value.serialize())
                context.append(OpcodeAssignStatic.from_reference(target, ref), self.source_ref)
                return True
            elif isinstance(self.value, Identifier):
                ref = context.resolve(self.value)
                context.append(OpcodeAssignLocal.from_references(target, ref), self.source_ref)
                return True

    def pull_up(self, target, context):
        if isinstance(target, Identifier):
            target_ref = context.resolve(target)
            context.append(OpcodePopLocal.from_reference(target_ref), self.source_ref)
        elif isinstance(target, NamedAccess):
            if target.extensions:
                target_ref = target.compile(context, pop_last=True)
            else:
                target_ref = context.resolve(target)
                context.append(OpcodePopMember.from_reference(target_ref), self.source_ref)
        else:
            raise Exception('Cannot pull up {}'.format(target))

        return target_ref

    @property
    def type(self):
        return self.name.type

    ASSIGNMENT_TARGET = Identifier, NamedAccess, IndexedAccess

    @staticmethod
    @ParserRule.mark
    def assignment_declaration(type_name: Identifier, name: Identifier, _: LexicalAssignment, value: ValueType):
        return AssignmentOperation(AssignmentOperation.DECELERATION, name, value, type_name)

    @staticmethod
    @ParserRule.mark
    def assignment_reassignment(name: ASSIGNMENT_TARGET, _: LexicalAssignment, value: ValueType):
        return AssignmentOperation(AssignmentOperation.REASSIGNMENT, name, value)

    @staticmethod
    @ParserRule.mark
    def in_place_modifier(name: ASSIGNMENT_TARGET, operator: LexicalBinaryOperation, _: LexicalAssignment, val: ValueType):
        return AssignmentOperation(AssignmentOperation.REASSIGNMENT, name, BinaryOperation(operator, name, val))
