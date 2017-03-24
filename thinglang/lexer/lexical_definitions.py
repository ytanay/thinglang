import re


from thinglang.lexer.symbols.logic import LexicalConditional, LexicalEquality, LexicalElse, LexicalNegation, \
    LexicalGreaterThan, LexicalLessThan, LexicalBooleanTrue, LexicalBooleanFalse
from thinglang.lexer.symbols.arithmetic import LexicalAddition, LexicalSubtraction, LexicalDivision, \
    LexicalMultiplication
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

    '>': LexicalGreaterThan,
    '<': LexicalLessThan,

    '#': LexicalInlineComment
}


KEYWORDS = {
    'thing': LexicalDeclarationThing,
    'does': LexicalDeclarationMethod,
    'with': LexicalArgumentListIndicator,
    'return': LexicalReturnStatement,
    'if': LexicalConditional,
    'otherwise': LexicalElse,

    'eq': LexicalEquality,
    'not': LexicalNegation,

    'true': LexicalBooleanTrue,
    'false': LexicalBooleanFalse
}


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))