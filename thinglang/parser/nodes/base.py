import struct

from thinglang.compiler import CompilationContext, LocalReference
from thinglang.compiler.opcodes import OpcodePopLocal, OpcodePushStatic, OpcodeAssignStatic, OpcodePopMember, \
    OpcodeAssignLocal, OpcodePushLocal, OpcodePushMember
from thinglang.foundation import definitions
from thinglang.lexer.tokens import LexicalToken
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.nodes.functions import MethodCall, Access
from thinglang.utils.type_descriptors import ValueType


class AssignmentOperation(BaseNode):
    DECELERATION = object()
    REASSIGNMENT = object()
    INDETERMINATE = object()

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
                return context.append(OpcodeAssignStatic.from_reference(target, ref))
            elif self.value.implements(LexicalIdentifier):
                ref = context.resolve(self.value)
                return context.append(OpcodeAssignLocal.from_references(target, ref))

        if self.value.implements(MethodCall):
            self.value.compile(context, True)
        else:
            self.value.compile(context)

        target = self.name
        if target.implements(LexicalIdentifier):
            target = context.resolve(target)
            context.append(OpcodePopLocal.from_reference(target))
        elif target.implements(Access):
            context.append(OpcodePopMember.local_reference(context.resolve(target)))

        else:
            raise Exception('Cannot pull up {}'.format(target))


class InlineString(LexicalToken, ValueType):  # immediate string e.g. "hello world"
    STATIC = True
    TYPE = LexicalIdentifier("text")
    TYPE_IDX = definitions.INTERNAL_TYPE_ORDERING[LexicalIdentifier("text")]

    def __init__(self, value):
        super().__init__(None)
        self.value = value

    def serialize(self):
        return struct.pack('<iI', self.TYPE_IDX, len(self.value)) + bytes(self.value, 'utf-8')

    def transpile(self):
        return f'"{self.value}"'

    @property
    def type(self):
        return self.TYPE

    def describe(self):
        return '"{}"'.format(self.value)

    def compile(self, context: CompilationContext):
        ref = context.append_static(self.serialize())
        context.append(OpcodePushStatic(ref))


class InlineCode(LexicalToken):
    STATIC = True
    SCOPING = False

    def __init__(self, value):
        super(InlineCode, self).__init__(None, value)
        self.children = []

    def tree(self, depth):
        return self.value
