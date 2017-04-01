from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalToken


class LexicalQuote(LexicalToken):  # "
    EMITTABLE = False

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


class LexicalInlineComment(LexicalToken): pass


class LexicalAssignment(LexicalToken): pass


class LexicalIdentifier(LexicalToken, ValueType):

    def __init__(self, value):
        super(LexicalIdentifier, self).__init__(value)
        self.value = value

    def describe(self):
        return self.value

    def evaluate(self, resolver):
        return resolver.resolve(self)

    def is_self(self):
        return self == LexicalIdentifier.SELF

    @classmethod
    def constructor(cls):
        return cls("constructor")

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value


LexicalIdentifier.SELF = LexicalIdentifier("self")
