import struct

from thinglang.compiler import CompilationContext, BytecodeSymbols
from thinglang.foundation import Foundation
from thinglang.lexer.tokens import LexicalToken
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import BaseSymbol
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.functions import MethodCall
from thinglang.utils.type_descriptors import ValueType


class AssignmentOperation(BaseSymbol):
    DECELERATION = object()
    REASSIGNMENT = object()
    INDETERMINATE = object()

    def __init__(self, slice):
        super(AssignmentOperation, self).__init__(slice)
        self.target = None
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
        if self.value.implements((MethodCall, ArithmeticOperation)):
            self.value.compile(context, captured=True)
            context.append(BytecodeSymbols.set(self.target))
        elif self.value.implements(LexicalIdentifier):
            context.append(BytecodeSymbols.copy(self.target, self.value))
        elif self.value.STATIC:
            context.append(BytecodeSymbols.set_static(self.target, context.append_static(self.value.serialize())))


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

    def type_id(self):
        return self.TYPE


class InlineCode(LexicalToken):
    STATIC = True
    SCOPING = False

    def __init__(self, value):
        super(InlineCode, self).__init__(None, value)
        self.children = []