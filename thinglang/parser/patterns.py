from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.symbols import LexicalGroupEnd
from thinglang.lexer.symbols.arithmetic import FirstOrderLexicalBinaryOperation, SecondOrderLexicalBinaryOperation
from thinglang.lexer.symbols.base import LexicalParenthesesOpen, LexicalParenthesesClose, LexicalSeparator, \
    LexicalAccess, LexicalAssignment, LexicalIdentifier, LexicalBracketOpen, LexicalBracketClose
from thinglang.lexer.symbols.functions import LexicalReturnStatement, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod, LexicalDeclarationThing, LexicalDeclarationMember, LexicalDeclarationConstructor, \
    LexicalClassInitialization
from thinglang.lexer.symbols.logic import LexicalComparison, LexicalConditional, LexicalElse, LexicalNegation, \
    LexicalEquality, LexicalInequality, LexicalRepeatWhile
from thinglang.parser.tokens.arithmetic import ArithmeticOperation
from thinglang.parser.tokens.base import AssignmentOperation
from thinglang.parser.tokens.classes import ThingDefinition, MethodDefinition, MemberDefinition
from thinglang.parser.tokens.functions import Access, ArgumentListPartial, ArgumentList, MethodCall, ReturnStatement, \
    ArgumentListDecelerationPartial
from thinglang.parser.tokens.types import ArrayInitializationPartial, ArrayInitialization
from thinglang.parser.tokens.types import ArrayInitializationPartial, ArrayInitialization, CastOperation
from thinglang.parser.tokens.logic import Conditional, UnconditionalElse, ConditionalElse, Loop

FIRST_PASS_PATTERNS = [

    ((LexicalDeclarationThing, LexicalIdentifier), ThingDefinition),  # thing Program
    ((LexicalDeclarationMethod, LexicalIdentifier, LexicalGroupEnd), MethodDefinition),  # does start
    ((LexicalDeclarationMethod, LexicalIdentifier, ArgumentList), MethodDefinition),  # does start with a, b
    ((LexicalDeclarationConstructor, ArgumentList), MethodDefinition),  # setup with a, b
    ((LexicalDeclarationConstructor, LexicalGroupEnd), MethodDefinition), # setup
    ((LexicalDeclarationMember, LexicalIdentifier, LexicalIdentifier), MemberDefinition),

    ((ValueType, LexicalCast, LexicalIdentifier), CastOperation),
    ((Access, ArgumentList), MethodCall),  # person.walk(...)

    ((LexicalArgumentListIndicator, ValueType), ArgumentListDecelerationPartial),  # with a

    ((LexicalIdentifier, LexicalAccess, LexicalIdentifier), Access),  # person.name

    ((ValueType, LexicalComparison, ValueType), ArithmeticOperation),  # x eq y
    ((LexicalNegation, LexicalEquality), LexicalInequality),

    ((ValueType, SecondOrderLexicalBinaryOperation, ValueType), ArithmeticOperation),  # 4 * 2
    ((ValueType, FirstOrderLexicalBinaryOperation, ValueType), ArithmeticOperation),  # 4 + 2

    ((ArgumentListPartial, SecondOrderLexicalBinaryOperation, ValueType), ArgumentListPartial),  # (4 * 2
    ((ArgumentListPartial, FirstOrderLexicalBinaryOperation, ValueType), ArgumentListPartial),  # (4 + 2

    ((LexicalParenthesesOpen, LexicalParenthesesClose), ArgumentList),  # ()

    ((LexicalParenthesesOpen, ValueType), ArgumentListPartial),  # (2

    ((LexicalBracketOpen, ValueType), ArrayInitializationPartial),  # [2
    ((ArrayInitializationPartial, LexicalSeparator, ValueType), ArrayInitializationPartial),  # (2, 3
    ((ArrayInitializationPartial, LexicalBracketClose), ArrayInitialization),  # (2, 3)

    ((ArgumentListDecelerationPartial, LexicalSeparator, ValueType), ArgumentListDecelerationPartial),  # (2, 3
    ((ArgumentListPartial, LexicalSeparator, ValueType), ArgumentListPartial),  # (2, 3

    ((ArgumentListPartial, LexicalParenthesesClose), ArgumentList),  # (2, 3)
    ((ArgumentListDecelerationPartial, LexicalGroupEnd), ArgumentList),  # (2, 3)


    ((LexicalConditional, ValueType), Conditional),  # if x
    ((LexicalRepeatWhile, ValueType), Loop),
    ((LexicalElse, Conditional), ConditionalElse),

    ((LexicalIdentifier, LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # number n = 1
    ((LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,
    ((Access, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,

    ((LexicalClassInitialization, LexicalIdentifier, ArgumentList), MethodCall)

]

SECOND_PASS_PATTERNS = [
    ((LexicalReturnStatement, ValueType), ReturnStatement),  # return 2
    ((LexicalElse,), UnconditionalElse)
]


REPLACEMENT_PASSES = FIRST_PASS_PATTERNS, SECOND_PASS_PATTERNS
