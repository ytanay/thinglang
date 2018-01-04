import struct

from thinglang.compiler import serializer
from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodePushStatic
from thinglang.foundation import definitions
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.primitive_type import PrimitiveType
from thinglang.utils.type_descriptors import ValueType


class InlineString(PrimitiveType):
    """
    Represents a constant inline string
    """

    TYPE = Identifier('text')
    PRIMITIVE_ID = definitions.PRIMITIVE_TYPES.index('text')

    def __init__(self, value, source_ref=None):
        super().__init__(value, source_ref)

    def serialize(self):
        return struct.pack('<i', InlineString.PRIMITIVE_ID) + serializer.auto(self.value)
