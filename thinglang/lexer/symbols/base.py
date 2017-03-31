from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.symbols import LexicalSymbol


class LexicalQuote(LexicalSymbol):  # "
    EMITTABLE = False

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'"': LexicalQuote}
        return original


class LexicalParenthesesOpen(LexicalSymbol):
    pass  # (


class LexicalParenthesesClose(LexicalSymbol):
    pass  # )


class LexicalBracketOpen(LexicalSymbol):
    pass  # [


class LexicalBracketClose(LexicalSymbol):
    pass  # ]


class LexicalSeparator(LexicalSymbol):
    pass  # ,


class LexicalIndent(LexicalSymbol):
    pass  # <TAB>


class LexicalAccess(LexicalSymbol):
    pass  # a.b


class LexicalInlineComment(LexicalSymbol): pass


class LexicalAssignment(LexicalSymbol): pass


class LexicalIdentifier(LexicalSymbol, ValueType):

    def __init__(self, value):
        super(LexicalIdentifier, self).__init__(value)
        self.value = value

    def describe(self):
        return self.value

    def evaluate(self, resolver):
        return resolver.resolve(self)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

LexicalIdentifier.SELF = LexicalIdentifier("self")