import re


from thinglang.lexer.symbols.logic import LexicalConditional, LexicalEquality, LexicalElse
from thinglang.lexer.symbols.arithmetic import FirstOrderLexicalBinaryOperation, SecondOrderLexicalBinaryOperation, \
    LexicalAddition, LexicalSubtraction, LexicalDivision, LexicalMultiplication
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

    '+': LexicalAddition,
    '-': LexicalSubtraction,
    '/': LexicalDivision,
    '*': LexicalMultiplication,

    '#': LexicalInlineComment
}


KEYWORDS = {
    'thing': LexicalDeclarationThing,
    'does': LexicalDeclarationMethod,
    'with': LexicalArgumentListIndicator,
    'return': LexicalReturnStatement,
    'if': LexicalConditional,
    'otherwise': LexicalElse,
    'eq': LexicalEquality
}


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))