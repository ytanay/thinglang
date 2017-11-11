from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.operators.comparison import LexicalLessThan, LexicalGreaterThan
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.mixins import ParsingMixin
from thinglang.utils.type_descriptors import ValueType


class Identifier(LexicalToken, ValueType, ParsingMixin):
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

    def __repr__(self):
        return '{}'.format(self.value)

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

    @property
    def untyped(self):
        return self


class GenericIdentifier(Identifier):

    def __init__(self, name, type=None, generic=None):
        super().__init__(name)
        self.name, self.type, self.generic = name, type, generic

    @staticmethod
    @ParserRule.mark
    def generic_declaration(name: Identifier, _1: LexicalLessThan, generic: Identifier, _2: LexicalGreaterThan):
        return GenericIdentifier(name, generic=generic)

    def __repr__(self):
        if self.generic:
            return f'{self.name}<{self.generic}>'
        return super().__repr__()

    @property
    def untyped(self):
        return self.name