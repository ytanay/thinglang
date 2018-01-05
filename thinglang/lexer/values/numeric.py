import struct

from thinglang.foundation import definitions
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.primitive_type import PrimitiveType


class NumericValue(PrimitiveType):
    """
    An inline numeric value
    """

    TYPE = Identifier("number")
    PRIMITIVE_ID = definitions.PRIMITIVE_TYPES.index('number')

    def __init__(self, value, source_ref=None):
        super(NumericValue, self).__init__(int(value), source_ref)

    def serialize(self):
        return struct.pack('<ii', NumericValue.PRIMITIVE_ID, self.value)

