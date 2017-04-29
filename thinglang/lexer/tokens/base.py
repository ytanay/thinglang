from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalToken


class LexicalQuote(LexicalToken):  # "
    EMITTABLE = False
    ALLOW_EMPTY = True

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'"': LexicalQuote}
        return original


class LexicalParenthesesOpen(LexicalToken):
    pass  # (


class LexicalParenthesesClose(LexicalToken):
    pass  # )


class LexicalBracketOpen(LexicalToken):
    pass  # [


class LexicalBracketClose(LexicalToken):
    pass  # ]


class LexicalSeparator(LexicalToken):
    pass  # ,


class LexicalIndent(LexicalToken):
    pass  # <TAB>


class LexicalAccess(LexicalToken):
    pass  # a.b


class LexicalInlineComment(LexicalToken):
    pass


class LexicalAssignment(LexicalToken):
    pass


class LexicalIdentifier(LexicalToken, ValueType):
    TYPE_INDICATOR = object()

    def __init__(self, value, type=None):
        super(LexicalIdentifier, self).__init__(value, value)
        self.type = type

    def __str__(self):
        return '{{{}:{}}}'.format(self.value, self.type) if self.type else '{{{}}}'.format(self.value)

    def evaluate(self, resolver):
        return resolver.resolve(self)

    def is_self(self):
        return self == LexicalIdentifier("self")

    @classmethod
    def constructor(cls):
        return cls("constructor")

    @classmethod
    def self(cls):
        return cls("self")

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

    def references(self):
        return self

    def transpile(self):
        if self.is_self():
            return 'this'
        return self.value