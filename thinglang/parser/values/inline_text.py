import struct

from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodePushStatic
from thinglang.foundation import definitions
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.values.identifier import Identifier
from thinglang.utils.type_descriptors import ValueType


class InlineString(LexicalToken, ValueType):
    """
    Represents a constant inline string
    """

    STATIC = True
    TYPE = Identifier("text")
    TYPE_IDX = definitions.INTERNAL_TYPE_ORDERING[Identifier("text")]

    def __init__(self, value, source_ref=None):
        super().__init__(value, source_ref)

    def serialize(self):
        return struct.pack('<iI', InlineString.PRIMITIVE_ID) + serializer.auto(self.value)

    @property
    def type(self):
        return self.TYPE

    def __repr__(self):
        return '"{}"'.format(self.value)

    def compile(self, context: CompilationBuffer):
        ref = context.append_static(self.serialize())
        context.append(OpcodePushStatic(ref), self.source_ref)
        return self
