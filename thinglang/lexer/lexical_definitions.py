import re

from thinglang.lexer.blocks.conditionals import LexicalConditional, LexicalElse
from thinglang.lexer.blocks.loops import LexicalRepeatFor, LexicalRepeatWhile
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationThing, LexicalDeclarationMember, \
    LexicalDeclarationConstructor, LexicalDeclarationStatic, LexicalDeclarationReturnType, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod
from thinglang.lexer.grouping.brackets import LexicalBracketOpen, LexicalBracketClose
from thinglang.lexer.grouping.parentheses import LexicalParenthesesOpen, LexicalParenthesesClose
from thinglang.lexer.grouping.quote import LexicalQuote
from thinglang.lexer.grouping.backtick import LexicalBacktick
from thinglang.lexer.operators.assignment import LexicalAssignment
from thinglang.lexer.operators.binary import LexicalAddition, LexicalSubtraction, LexicalMultiplication, \
    LexicalDivision
from thinglang.lexer.operators.casts import LexicalCast
from thinglang.lexer.operators.comparison import LexicalEquals, LexicalNegation, LexicalGreaterThan, \
    LexicalLessThan
from thinglang.lexer.operators.membership import LexicalIn
from thinglang.lexer.statements.return_statement import LexicalReturnStatement
from thinglang.lexer.statements.thing_instantiation import LexicalThingInstantiation
from thinglang.lexer.tokens.inline_comment import LexicalInlineComment
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.tokens.indent import LexicalIndent
from thinglang.lexer.tokens.separator import LexicalSeparator
from thinglang.lexer.values.booleans import LexicalBooleanTrue, LexicalBooleanFalse

IDENTIFIER_BASE = r"[a-zA-Z]\w*"
IDENTIFIER_STANDALONE = re.compile("^" + IDENTIFIER_BASE + "$")

OPERATORS = {
    ' ': None,

    '"': LexicalQuote,
    '`': LexicalBacktick,
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

    'create': LexicalThingInstantiation,

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
    LexicalEquals: "=="
})
