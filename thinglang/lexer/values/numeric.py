import struct

from thinglang.compiler.opcodes import OpcodePushStatic
from thinglang.foundation import definitions
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.values.identifier import Identifier
from thinglang.utils.type_descriptors import ValueType


class NumericValue(LexicalToken, ValueType):
    """
    An inline numeric value
    """

    STATIC = True
    TYPE = Identifier("number")
    TYPE_IDX = definitions.INTERNAL_TYPE_ORDERING[Identifier("number")]

    def __init__(self, value, source_ref=None):
        super(NumericValue, self).__init__(value, source_ref)
        self.value = int(value)

    def evaluate(self, _=None):
        return self.value

    def describe(self):
        return self.value

    def serialize(self):
        return struct.pack('<ii', self.TYPE_IDX, self.value)

    @property
    def type(self):
        return self.TYPE

    def compile(self, context):
        ref = context.append_static(self.serialize())
        context.append(OpcodePushStatic(ref), self.source_ref)
        return self

    def __repr__(self):
        return f'{{{self.value}}}'