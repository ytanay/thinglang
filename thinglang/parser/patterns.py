import collections

from thinglang.lexer.tokens.typing import LexicalCast
from thinglang.parser.symbols.collections import ListInitializationPartial, ListInitialization
from thinglang.parser.symbols.proxies import ConstrainedArithmeticOperation
from thinglang.utils.type_descriptors import ValueType
from thinglang.lexer.tokens import LexicalGroupEnd
from thinglang.lexer.tokens.arithmetic import FirstOrderLexicalBinaryOperation, SecondOrderLexicalBinaryOperation
from thinglang.lexer.tokens.base import LexicalParenthesesOpen, LexicalParenthesesClose, LexicalSeparator, \
    LexicalAccess, LexicalAssignment, LexicalIdentifier, LexicalBracketOpen, LexicalBracketClose
from thinglang.lexer.tokens.functions import LexicalReturnStatement, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod, LexicalDeclarationThing, LexicalDeclarationMember, LexicalDeclarationConstructor, \
    LexicalClassInitialization
from thinglang.lexer.tokens.logic import LexicalComparison, LexicalConditional, LexicalElse, LexicalNegation, \
    LexicalEquality, LexicalInequality, LexicalRepeatWhile
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.classes import ThingDefinition, MethodDefinition, MemberDefinition
from thinglang.parser.symbols.functions import Access, ArgumentListPartial, ArgumentList, MethodCall, ReturnStatement, \
    ArgumentListDecelerationPartial
from thinglang.parser.symbols.types import ArrayInitializationPartial, ArrayInitialization, CastOperation
from thinglang.parser.symbols.logic import Conditional, UnconditionalElse, ConditionalElse, Loop
from thinglang.utils.union_types import POTENTIALLY_RESOLVABLE

FIRST_PASS_PATTERNS = collections.OrderedDict([  # Ordering is highly significant in parsing patterns

    ((LexicalDeclarationThing, LexicalIdentifier), ThingDefinition),  # thing Program
    ((LexicalDeclarationMethod, LexicalIdentifier, LexicalGroupEnd), MethodDefinition),  # does start
    ((LexicalDeclarationMethod, LexicalIdentifier, ArgumentList), MethodDefinition),  # does start with a, b
    ((LexicalDeclarationConstructor, ArgumentList), MethodDefinition),  # setup with a, b
    ((LexicalDeclarationConstructor, LexicalGroupEnd), MethodDefinition),  # setup
    ((LexicalDeclarationMember, LexicalIdentifier, LexicalIdentifier), MemberDefinition),

    ((ValueType, LexicalCast, LexicalIdentifier), CastOperation),

    ((Access, ArgumentList), MethodCall),  # person.walk(...)

    ((LexicalArgumentListIndicator, ValueType), ArgumentListDecelerationPartial),  # with a

    ((LexicalIdentifier, LexicalAccess, LexicalIdentifier), Access),  # person.name

    ((ValueType, LexicalComparison, ValueType), ArithmeticOperation),  # x eq y
    ((LexicalNegation, LexicalEquality), LexicalInequality),

    ((ArgumentListPartial, SecondOrderLexicalBinaryOperation, ValueType), ArgumentListPartial),  # (4 * 2
    ((ArgumentListPartial, FirstOrderLexicalBinaryOperation, ValueType), ArgumentListPartial),  # (4 + 2

    ((LexicalParenthesesOpen, LexicalParenthesesClose), ArgumentList),  # ()

    ((LexicalParenthesesOpen, ValueType), ArgumentListPartial),  # (2

    ((LexicalBracketOpen, ValueType), ArrayInitializationPartial),  # [2
    ((ArrayInitializationPartial, LexicalSeparator, ValueType), ArrayInitializationPartial),  # (2, 3
    ((ArrayInitializationPartial, LexicalBracketClose), ArrayInitialization),  # (2, 3)

    ((ArgumentListDecelerationPartial, LexicalSeparator, ValueType), ArgumentListDecelerationPartial),  # (2, 3
    ((ArgumentListPartial, LexicalSeparator, ValueType), ArgumentListPartial),  # (2, 3
    ((ArgumentListPartial, ArgumentList), ArgumentListPartial),

    ((ArgumentListPartial, LexicalParenthesesClose), ArgumentList),  # (2, 3)
    ((ArgumentListDecelerationPartial, LexicalGroupEnd), ArgumentList),  # (2, 3)

    ((POTENTIALLY_RESOLVABLE, SecondOrderLexicalBinaryOperation, POTENTIALLY_RESOLVABLE), ArithmeticOperation),  # 4 * 2
    ((POTENTIALLY_RESOLVABLE, FirstOrderLexicalBinaryOperation, POTENTIALLY_RESOLVABLE), ArithmeticOperation),  # 4 + 2

    ((ListInitializationPartial, SecondOrderLexicalBinaryOperation, ListInitialization), ConstrainedArithmeticOperation),  # 4 * 2
    ((ListInitializationPartial, FirstOrderLexicalBinaryOperation, ListInitialization), ConstrainedArithmeticOperation),  # 4 + 2


    ((LexicalConditional, ValueType), Conditional),  # if x
    ((LexicalRepeatWhile, ValueType), Loop),
    ((LexicalElse, Conditional), ConditionalElse),

    ((LexicalIdentifier, LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # number n = 1
    ((LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,
    ((Access, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,

    ((LexicalClassInitialization, LexicalIdentifier, ArgumentList), MethodCall),

    ((ArgumentListPartial, LexicalSeparator, POTENTIALLY_RESOLVABLE), ArgumentListPartial), # To deal with Access in argument lists

])

SECOND_PASS_PATTERNS = collections.OrderedDict([
    ((LexicalReturnStatement, ValueType), ReturnStatement),  # return 2
    ((LexicalElse,), UnconditionalElse),
    ((LexicalIdentifier, ArgumentList), MethodCall),  # person.walk(...)
])


REPLACEMENT_PASSES = FIRST_PASS_PATTERNS, SECOND_PASS_PATTERNS
