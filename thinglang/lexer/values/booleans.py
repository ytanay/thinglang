import struct

from thinglang.compiler.opcodes import OpcodePushStatic
from thinglang.foundation import definitions
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.primitive_type import PrimitiveType
from thinglang.utils.type_descriptors import ValueType


class LexicalBoolean(PrimitiveType):
    """
    The base boolean type.
    """

    TYPE = Identifier("bool")
    PRIMITIVE_ID = definitions.PRIMITIVE_TYPES.index('number')

    def __init__(self, value, source_ref=None):
        super(LexicalBoolean, self).__init__(value, source_ref)
        self.value = bool(value)

    def serialize(self):
        return struct.pack('<ii', LexicalBoolean.PRIMITIVE_ID, self.value)


class LexicalBooleanTrue(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanTrue, self).__init__(True, source_ref)


class LexicalBooleanFalse(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanFalse, self).__init__(False, source_ref)
