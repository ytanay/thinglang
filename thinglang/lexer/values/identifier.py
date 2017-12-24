from thinglang.lexer.lexical_token import LexicalToken
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

    def parameterize(self, parameters):
        if self in parameters:
            return parameters[self]
        return self

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

    def __len__(self):
        return len(self.value)

    @classmethod
    def constructor(cls):
        return cls("__constructor__")

    @classmethod
    def self(cls):
        return cls("self")

    @classmethod
    def object(cls):
        return cls("object")

    @classmethod
    def super(cls):
        return cls("super")

    @property
    def untyped(self):
        return self


class GenericIdentifier(Identifier):

    def __init__(self, name, generics=None):
        super().__init__(name, name.source_ref)
        assert isinstance(generics, tuple), type(generics)
        self.generics = generics

    def parameterize(self, parameters):
        return GenericIdentifier(self.value, tuple(x.parameterize(parameters) for x in self.generics))

    @property
    def untyped(self):
        return self.value

    def serialize(self):
        return [self.value, self.generics]

    @classmethod
    def wrap(cls, name, generic):
        return cls(Identifier(name), (Identifier(generic) if isinstance(generic, str) else generic,))

    @staticmethod
    @ParserRule.mark
    def generic_declaration(name: Identifier, generic: 'ParameterVector'):
        return GenericIdentifier(name, generic)

    def __repr__(self):
        if self.generics:
            return f'{self.value}<{self.generics}>'
        return super().__repr__()

    def __eq__(self, other):
        return type(self) is type(other) and \
               self.value == other.value and \
               (self.generics == other.generics or self.generics == (Identifier.object(),) or other.generics == (Identifier.object(),))

    def __hash__(self):
        return hash((self.value, self.generics))
