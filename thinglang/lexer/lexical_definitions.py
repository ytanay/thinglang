import re


from thinglang.lexer.tokens.logic import LexicalConditional, LexicalEquals, LexicalElse, LexicalNegation, \
    LexicalGreaterThan, LexicalLessThan, LexicalBooleanTrue, LexicalBooleanFalse, LexicalRepeatWhile, \
    LexicalIn, LexicalRepeatFor, LexicalInequality
from thinglang.lexer.tokens.arithmetic import LexicalAddition, LexicalSubtraction, LexicalDivision, \
    LexicalMultiplication
from thinglang.lexer.tokens.base import LexicalParenthesesOpen, LexicalParenthesesClose, LexicalQuote, LexicalSeparator, \
    LexicalIndent, LexicalAccess, LexicalInlineComment, LexicalAssignment, LexicalBracketOpen, LexicalBracketClose, \
    LexicalTick
from thinglang.lexer.tokens.functions import LexicalReturnStatement, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod, LexicalDeclarationThing, LexicalDeclarationMember, LexicalDeclarationConstructor, \
    LexicalClassInitialization, LexicalDeclarationReturnType, LexicalDeclarationStatic
from thinglang.lexer.tokens.typing import LexicalCast

IDENTIFIER_BASE = r"[a-zA-Z]\w*"
IDENTIFIER_STANDALONE = re.compile("^" + IDENTIFIER_BASE + "$")

OPERATORS = {
    ' ': None,

    '"': LexicalQuote,
    '`': LexicalTick,
    '\t': LexicalIndent,

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
    'static': LexicalDeclarationStatic,
    'has': LexicalDeclarationMember,
    'setup': LexicalDeclarationConstructor,
    'returns': LexicalDeclarationReturnType,

    'create': LexicalClassInitialization,

    'with': LexicalArgumentListIndicator,
    'return': LexicalReturnStatement,

    'if': LexicalConditional,
    'otherwise': LexicalElse,

    'while': LexicalRepeatWhile,
    'in': LexicalIn,
    'for': LexicalRepeatFor,

    'eq': LexicalEquals,
    'not': LexicalNegation,

    'true': LexicalBooleanTrue,
    'false': LexicalBooleanFalse,

    'as': LexicalCast
}

REVERSE_OPERATORS = {
    v: k for k, v in OPERATORS.items()
}

REVERSE_OPERATORS.update({
    LexicalEquals: "==",
    LexicalInequality: '!='
})
