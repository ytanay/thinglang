import re

from thinglang.lexer.lexical_tokens import LexicalParenthesesClose, LexicalQuote, LexicalSeparator, LexicalIndent, LexicalParenthesesOpen, LexicalAccess, \
    LexicalDeclarationThing, LexicalDeclarationMethod, \
    LexicalAssignment, FirstOrderLexicalBinary, SecondOrderLexicalBinary, LexicalArgumentListIndicator, \
    LexicalInlineComment

IDENTIFIER_BASE = r"[a-zA-Z]\w*"
IDENTIFIER = re.compile(IDENTIFIER_BASE)
IDENTIFIER_STANDALONE = re.compile("^" + IDENTIFIER_BASE + "$")

OPERATORS = {
    ' ': None,
    '(': LexicalParenthesesOpen,
    ')': LexicalParenthesesClose,
    '.': LexicalAccess,

    "\"": LexicalQuote,
    ',': LexicalSeparator,
    "\t": LexicalIndent,

    '=': LexicalAssignment,

    '+': FirstOrderLexicalBinary,
    '-': FirstOrderLexicalBinary,
    '/': SecondOrderLexicalBinary,
    '*': SecondOrderLexicalBinary,

    '#': LexicalInlineComment
}


KEYWORDS = {
    'thing': LexicalDeclarationThing,
    'does': LexicalDeclarationMethod,
    'with': LexicalArgumentListIndicator
}


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))