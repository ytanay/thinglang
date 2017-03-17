import re


from thinglang.lexer.symbols.logic import LexicalConditional, LexicalEquality
from thinglang.lexer.symbols.arithmetic import FirstOrderLexicalBinaryOperation, SecondOrderLexicalBinaryOperation
from thinglang.lexer.symbols.base import LexicalParenthesesOpen, LexicalParenthesesClose, LexicalQuote, LexicalSeparator, \
    LexicalIndent, LexicalAccess, LexicalInlineComment, LexicalAssignment
from thinglang.lexer.symbols.functions import LexicalReturnStatement, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod, LexicalDeclarationThing

IDENTIFIER_BASE = r"[a-zA-Z]\w*"
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

    '+': FirstOrderLexicalBinaryOperation,
    '-': FirstOrderLexicalBinaryOperation,
    '/': SecondOrderLexicalBinaryOperation,
    '*': SecondOrderLexicalBinaryOperation,

    '#': LexicalInlineComment
}


KEYWORDS = {
    'thing': LexicalDeclarationThing,
    'does': LexicalDeclarationMethod,
    'with': LexicalArgumentListIndicator,
    'return': LexicalReturnStatement,
    'if': LexicalConditional,
    'eq': LexicalEquality
}


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))