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


class LexicalTick(LexicalToken):  # `
    EMITTABLE = False
    ALLOW_EMPTY = True

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'`': LexicalTick}
        return original


class LexicalParenthesesOpen(LexicalToken):

    pass  # (


class LexicalParenthesesClose(LexicalToken):
    MUST_CLOSE = True
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
    def __init__(self, value, type=None):
        super(LexicalIdentifier, self).__init__(value, value)
        self.type = type
        self.index = None

    def compile(self, context):
        context.push_ref(context.resolve(self))

    def transpile(self):
        return self.value

    def upper(self):
        return self.value.upper()

    def __str__(self):
        return '<{}>'.format(self.value)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return type(other) == type(self) and self.value == other.value

    @classmethod
    def constructor(cls):
        return cls("constructor")

    @classmethod
    def self(cls):
        return cls("self")
