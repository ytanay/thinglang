from thinglang.compiler.opcodes import OpcodePushStatic
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.utils.type_descriptors import ValueType


class PrimitiveType(LexicalToken, ValueType):
    """
    The base boolean type.
    """

    STATIC = True
    TYPE = None
    PRIMITIVE_ID = None

    def __init__(self, value, source_ref=None):
        super(PrimitiveType, self).__init__(value, source_ref)

    def evaluate(self, _=None):
        return self.value

    @property
    def type(self):
        return self.TYPE

    def serialize(self):
        raise NotImplementedError('Primitive types must implement serialize')

    def compile(self, context):
        ref = context.append_static(self.serialize())
        context.append(OpcodePushStatic(ref), self.source_ref)
        return self

    def __repr__(self):
        return f'{self.value}'
