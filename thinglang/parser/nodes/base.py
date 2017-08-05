import struct

from thinglang.compiler import CompilationContext, LocalReference
from thinglang.compiler.opcodes import OpcodeSetLocalStatic, OpcodePopLocal, OpcodeSetMember, OpcodePushStatic
from thinglang.foundation import Foundation
from thinglang.lexer.tokens import LexicalToken
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.nodes.functions import MethodCall
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

    def references(self):
        return (self.name, self.value.references()) if self.intent is self.REASSIGNMENT else self.value.references()

    @classmethod
    def create(cls, name, value, type=None):
        return cls(([type] if type is not None else []) + [name, None, value])

    def transpile(self):
        if self.intent is self.DECELERATION:
            return 'auto {} = {};'.format(self.name.transpile(), self.value.transpile())
        elif self.intent is self.REASSIGNMENT:
            return '{} = {};'.format(self.name.transpile(), self.value.transpile())

    def compile(self, context: CompilationContext):
        target = context.resolve(self.name)
        set_cls = OpcodeSetLocalStatic if isinstance(target, LocalReference) else OpcodeSetMember
        if self.value.STATIC:
            data_id = context.append_static(self.value.serialize())
            if isinstance(target, LocalReference):
                context.append(OpcodeSetLocalStatic(target, data_id))
            else:
                context.append(OpcodePushStatic(data_id))  # TODO: maybe add another argument?
                context.append(OpcodeSetMember(target))
        elif self.value.implements(MethodCall):
            self.value.compile(context, True)
            context.append(OpcodePopLocal(target))
        else:
            raise Exception('Unknown value type {}'.format(self.value))


class InlineString(LexicalToken, ValueType):  # immediate string e.g. "hello world"
    STATIC = True
    TYPE = LexicalIdentifier("text")
    TYPE_IDX = Foundation.INTERNAL_TYPE_ORDERING[LexicalIdentifier("text")]

    def __init__(self, value):
        super().__init__(None)
        self.value = value

    def evaluate(self, _):
        return self.value

    def serialize(self):
        return struct.pack('<iI', self.TYPE_IDX, len(self.value)) + bytes(self.value, 'utf-8')

    def references(self):
        return ()

    def transpile(self):
        return f'"{self.value}"'

    @property
    def type(self):
        return self.TYPE

    def describe(self):
        return '"{}"'.format(self.value)


class InlineCode(LexicalToken):
    STATIC = True
    SCOPING = False

    def __init__(self, value):
        super(InlineCode, self).__init__(None, value)
        self.children = []

    def tree(self, depth):
        return self.value
