from thinglang.lexer.lexical_token import LexicalToken
from thinglang.utils.type_descriptors import ValueType


class Identifier(LexicalToken, ValueType):
    """
    Identifiers can refer to local variables or as components of an Access object.
    """

    def __init__(self, value, source_ref=None):
        super(Identifier, self).__init__(value, source_ref)
        self.type = None
        self.index = None

    def compile(self, context):
        return context.push_ref(context.resolve(self), self.source_ref)

    def transpile(self):
        if self == Identifier.constructor():
            return '__constructor__'
        return self.value

    def upper(self):
        return self.value.upper()

    def __str__(self):
        return '<{}>'.format(self.value)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

    def __add__(self, other):
        return Identifier(self.value + other.value)

    @classmethod
    def constructor(cls):
        return cls("__constructor__")

    @classmethod
    def self(cls):
        return cls("self")
