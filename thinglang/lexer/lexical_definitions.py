import re


from thinglang.lexer.symbols.logic import LexicalConditional, LexicalEquality, LexicalElse, LexicalNegation, \
    LexicalGreaterThan, LexicalLessThan, LexicalBooleanTrue, LexicalBooleanFalse, LexicalRepeat, LexicalRepeatWhile
from thinglang.lexer.symbols.arithmetic import LexicalAddition, LexicalSubtraction, LexicalDivision, \
    LexicalMultiplication
from thinglang.lexer.symbols.base import LexicalParenthesesOpen, LexicalParenthesesClose, LexicalQuote, LexicalSeparator, \
    LexicalIndent, LexicalAccess, LexicalInlineComment, LexicalAssignment, LexicalBracketOpen, LexicalBracketClose
from thinglang.lexer.symbols.functions import LexicalReturnStatement, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod, LexicalDeclarationThing, LexicalDeclarationMember, LexicalDeclarationConstructor, \
    LexicalClassInitialization

IDENTIFIER_BASE = r"[a-zA-Z]\w*"
IDENTIFIER_STANDALONE = re.compile("^" + IDENTIFIER_BASE + "$")

OPERATORS = {
    ' ': None,

    "\"": LexicalQuote,
    "\t": LexicalIndent,

    '.': LexicalAccess,
    ',': LexicalSeparator,
    '=': LexicalAssignment,

    '(': LexicalParenthesesOpen,
    ')': LexicalParenthesesClose,

    '[': LexicalBracketOpen,
    ']': LexicalBracketClose,

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
    'has': LexicalDeclarationMember,
    'created': LexicalDeclarationConstructor,

    'create': LexicalClassInitialization,

    'with': LexicalArgumentListIndicator,
    'return': LexicalReturnStatement,

    'if': LexicalConditional,
    'otherwise': LexicalElse,

    'repeat': LexicalRepeat,
    'while': LexicalRepeatWhile,

    'eq': LexicalEquality,
    'not': LexicalNegation,

    'true': LexicalBooleanTrue,
    'false': LexicalBooleanFalse
}


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))