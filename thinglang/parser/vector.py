import collections

from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.tokens.misc import LexicalGroupEnd
from thinglang.lexer.operators.binary import FirstOrderLexicalBinaryOperation, SecondOrderLexicalBinaryOperation
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.tokens.indent import LexicalIndent
from thinglang.lexer.tokens.separator import LexicalSeparator
from thinglang.lexer.grouping.parentheses import LexicalParenthesesOpen, LexicalParenthesesClose
from thinglang.lexer.operators.assignment import LexicalAssignment
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.statements.thing_instantiation import LexicalThingInstantiation
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationThing, LexicalDeclarationMember, \
    LexicalDeclarationConstructor, LexicalDeclarationStatic, LexicalDeclarationReturnType, LexicalArgumentListIndicator, \
    LexicalDeclarationMethod
from thinglang.lexer.statements.return_statement import LexicalReturnStatement
from thinglang.lexer.blocks.loops import LexicalRepeatWhile
from thinglang.lexer.blocks.conditionals import LexicalConditional, LexicalElse
from thinglang.lexer.operators.comparison import LexicalComparison
from thinglang.parser.blocks.conditional import Conditional
from thinglang.parser.blocks.conditional_else import ConditionalElse
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.blocks.unconditional_else import UnconditionalElse
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.definitions.tagged_definition import TaggedDeclaration
from thinglang.parser.definitions.thing_definition import ThingDefinition
from thinglang.parser.errors import VectorReductionError
from thinglang.parser.nodes import BaseNode
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.parser.statements.return_statement import ReturnStatement
from thinglang.parser.values.access import Access
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.parser.values.inline_code import InlineCode
from thinglang.parser.values.method_call import MethodCall
from thinglang.utils import collection_utils
from thinglang.utils.type_descriptors import ValueType


class TokenVector(object):

    def __init__(self, tokens=None):
        self.tokens = tokens if tokens is not None else []

    def parse(self) -> BaseNode:
        """
        Iteratively parses the token vector until a single node remains, or no further rule replacements can be made.
        """
        while self.perform_replacements():
            pass

        self.process_indentation()

        if len(self.tokens) != 1 or not isinstance(self.tokens[0], (ValueType, BaseNode)):
            raise VectorReductionError('Could not reduce vector: {}'.format(self.tokens))

        return self.tokens[0]

    def perform_replacements(self):
        """
        Given a list of lexical tokens, attempt to find partial matches, in order, using the replacements list defined above.
        Whenever a match succeeds, the matching slice is spliced out of place, and replaced with a parsed token instance.
        The list is modified in place.
        :return: True if a replacement occurred, None otherwise
        """
        for pattern, target in PATTERNS.items():
            start_matches = self.matching_starts(pattern[0])
            size = len(pattern)

            for match_start in start_matches:
                token_slice = self.tokens[match_start:match_start + size]

                if self.matches(pattern, token_slice):
                    token_slice = self.finalize_slice(token_slice)
                    self.tokens[match_start:match_start + size] = [target.construct(token_slice)]
                    return True

    def matching_starts(self, type_cls):
        """
        Returns the index of every element that is an instance of type_cls
        """
        return [idx for idx, entity in enumerate(self) if isinstance(entity, type_cls)]

    @staticmethod
    def matches(pattern, token_slice):
        """
        Checks if a list matches a pattern exactly.
        """
        if len(pattern) != len(token_slice):
            return False

        for type, instance in zip(pattern, token_slice):
            if not isinstance(instance, type):
                return False

        return True

    @staticmethod
    def finalize_slice(token_slice):
        """
        Parses all nested vectors in a slice
        """
        return [token.parse() if isinstance(token, TokenVector) else token for token in token_slice]

    def process_indentation(self):
        """
        Converts a list of LEXICAL_INDENTATION tokens at the beginning of a parsed group into indentation value stored on the first real token.
        """
        if isinstance(self.tokens[-1], LexicalGroupEnd):
            self.tokens[-1:] = []

        if not isinstance(self.tokens[0], LexicalIndent):
            return

        iterable = iter(self.tokens)
        size = 0

        while isinstance(next(iterable), LexicalIndent):
            size += 1

        self.tokens[0:size] = []

        if self.tokens:
            self.tokens[0].indent = size

    def append(self, token: LexicalToken):
        """
        Append a token to this vector
        """
        self.tokens.append(token)

    @property
    def empty(self):
        """
        Returns whether this token vector is effectively empty
        """
        return all(isinstance(x, (LexicalIndent, LexicalGroupEnd)) for x in self.tokens)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, item):
        return self.tokens[item]


class ParenthesesVector(TokenVector, ValueType):
    """
    Describes a vector of tokens bounded in parentheses, such as those in a method call's arguments or those
    signifying order-of-operations in an arithmetic operations
    """

    def parse(self):
        if not self.tokens:
            return []

        if not any(isinstance(token, LexicalSeparator) for token in self.tokens):
            return super().parse()

        groups = [TokenVector()]
        for token in self.tokens:
            if isinstance(token, LexicalSeparator):
                groups.append(TokenVector())
            else:
                groups[-1].append(token)

        return [group.parse() for group in groups]


class TypeVector(TokenVector):
    """
    Describes a vector of type pairings, such as those describing method arguments (e.g. number value, text name)
    """

    def parse(self):
        output = []

        if not all(isinstance(x, (Identifier, LexicalSeparator)) for x in self.tokens):
            raise ValueError('Only types, names and separators are allowed in a type vector')

        if len(self.tokens) < 2:
            raise ValueError('Not enough items in a type vector')

        for components in collection_utils.chunks(self.tokens, 3):
            if len(components) < 2 or not isinstance(components[0], Identifier) or not isinstance(components[1], Identifier):
                raise ValueError('Invalid syntax in type vector element - must be 2 consecutive names')

            if len(components) > 2 and not isinstance(components[2], LexicalSeparator):
                raise ValueError('Expected separator, got {}'.format(components[1]))

            components[1].type = components[0]
            output.append(components[1])

        return output


VECTOR_CREATION_TOKENS = {
    LexicalParenthesesOpen: (LexicalParenthesesClose, ParenthesesVector),
    LexicalArgumentListIndicator: ((LexicalDeclarationReturnType, LexicalGroupEnd), TypeVector)
}


METHOD_ID = (Identifier,) + tuple(BinaryOperation.OPERATIONS.keys())

PATTERNS = collections.OrderedDict([
    ((LexicalDeclarationThing, Identifier), ThingDefinition),  # thing Program
    ((LexicalDeclarationMember, (InlineCode, Identifier), Identifier), MemberDefinition),

    ((LexicalDeclarationStatic, LexicalDeclarationMethod), TaggedDeclaration),
    ((LexicalDeclarationMethod, METHOD_ID, TypeVector, LexicalDeclarationReturnType, Identifier), MethodDefinition),  # does compute with number a
    ((LexicalDeclarationMethod, METHOD_ID, TypeVector), MethodDefinition),  # does compute with number a
    ((LexicalDeclarationMethod, METHOD_ID, LexicalDeclarationReturnType, Identifier), MethodDefinition),  # does compute with number a
    ((LexicalDeclarationMethod, METHOD_ID), MethodDefinition),  # does say_hello
    ((LexicalDeclarationConstructor, TypeVector), MethodDefinition),  # setup with text name
    ((LexicalDeclarationConstructor,), MethodDefinition),  # setup

    ((Access, LexicalAccess, Identifier), Access),  # person.info.name
    ((Identifier, LexicalAccess, Identifier), Access),  # person.info

    ((Access, ParenthesesVector), MethodCall),
    ((LexicalThingInstantiation, Identifier, ParenthesesVector), MethodCall), # TODO: consider removing this syntax

    ((ValueType, SecondOrderLexicalBinaryOperation, ValueType), BinaryOperation),  # 4 * 2
    ((ValueType, FirstOrderLexicalBinaryOperation, ValueType), BinaryOperation),  # 4 + 2
    ((ValueType, LexicalComparison, ValueType), BinaryOperation),  # 4 == 2


    ((Identifier, Identifier, LexicalAssignment, ValueType), AssignmentOperation),  # number n = 1
    ((Identifier, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,
    ((Access, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,

    ((LexicalReturnStatement, ValueType), ReturnStatement),  # return 2
    ((LexicalReturnStatement,), ReturnStatement),

    ((LexicalConditional, ValueType), Conditional),  # if x
    ((LexicalElse, Conditional), ConditionalElse),
    ((LexicalElse,), UnconditionalElse),

    ((LexicalRepeatWhile, ValueType), Loop),  # repeat while
])
