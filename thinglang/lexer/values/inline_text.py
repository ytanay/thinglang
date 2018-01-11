import struct

from thinglang.compiler import serializer
from thinglang.foundation import definitions
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.primitive_type import PrimitiveType


class InlineString(PrimitiveType):
    """
    Represents a constant inline string
    """

    TYPE = Identifier('text')
    PRIMITIVE_ID = definitions.PRIMITIVE_TYPES.index('text')

    def __init__(self, value, source_ref=None):
        super().__init__(self.process_escaping(value), source_ref)

    def serialize(self):
        return struct.pack('<i', InlineString.PRIMITIVE_ID) + serializer.auto(self.value)

    @staticmethod
    def process_escaping(value):
        return bytes(value, 'utf-8').decode('unicode_escape')