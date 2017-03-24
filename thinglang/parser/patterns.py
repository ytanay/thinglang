from thinglang.common import ValueType
from thinglang.lexer.symbols import LexicalGroupEnd
from thinglang.lexer.symbols.arithmetic import FirstOrderLexicalBinaryOperation, SecondOrderLexicalBinaryOperation
from thinglang.lexer.symbols.base import LexicalParenthesesOpen, LexicalParenthesesClose, LexicalSeparator, \
    LexicalAccess, LexicalAssignment, LexicalIdentifier
from thinglang.lexer.symbols.functions import LexicalReturnStatement, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod, LexicalDeclarationThing
from thinglang.lexer.symbols.logic import LexicalComparison, LexicalConditional, LexicalElse, LexicalNegation, \
    LexicalEquality, LexicalInequality
from thinglang.parser.tokens.arithmetic import ArithmeticOperation, ComparisonOperation
from thinglang.parser.tokens.base import AssignmentOperation
from thinglang.parser.tokens.classes import ThingDefinition, MethodDefinition
from thinglang.parser.tokens.functions import Access, ArgumentListPartial, ArgumentList, MethodCall, ReturnStatement, \
    ArgumentListDecelerationPartial
from thinglang.parser.tokens.logic import Conditional, UnconditionalElse, ConditionalElse

FIRST_PASS_PATTERNS = [

    ((LexicalDeclarationThing, LexicalIdentifier), ThingDefinition),  # thing Program
    ((LexicalDeclarationMethod, LexicalIdentifier, LexicalGroupEnd), MethodDefinition),  # does start
    ((LexicalDeclarationMethod, LexicalIdentifier, ArgumentList), MethodDefinition),  # does start with a, b

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


    ((ArgumentListDecelerationPartial, LexicalSeparator, ValueType), ArgumentListDecelerationPartial),  # (2, 3
    ((ArgumentListPartial, LexicalSeparator, ValueType), ArgumentListPartial),  # (2, 3

    ((ArgumentListPartial, LexicalParenthesesClose), ArgumentList),  # (2, 3)
    ((ArgumentListDecelerationPartial, LexicalGroupEnd), ArgumentList),  # (2, 3)


    ((LexicalConditional, ValueType), Conditional),  # if x
    ((LexicalElse, Conditional), ConditionalElse),

    ((Access, ArgumentList), MethodCall),  # person.walk(...)

    ((LexicalIdentifier, LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # number n = 1
    ((LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,

]

SECOND_PASS_PATTERNS = [
    ((LexicalReturnStatement, ValueType), ReturnStatement),  # return 2
    ((LexicalElse,), UnconditionalElse),

]


REPLACEMENT_PASSES = FIRST_PASS_PATTERNS, SECOND_PASS_PATTERNS
