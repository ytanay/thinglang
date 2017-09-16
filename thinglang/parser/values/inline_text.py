import struct

from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodePushStatic
from thinglang.foundation import definitions
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.values.identifier import Identifier
from thinglang.utils.type_descriptors import ValueType


class InlineString(LexicalToken, ValueType):  # immediate string e.g. "hello world"
    STATIC = True
    TYPE = Identifier("text")
    TYPE_IDX = definitions.INTERNAL_TYPE_ORDERING[Identifier("text")]

    def __init__(self, value, source_ref=None):
        super().__init__(value, source_ref)

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
        context.append(OpcodePushStatic(ref), self.source_ref)
        return self
