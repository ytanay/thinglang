from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.tokens.indent import LexicalIndent
from thinglang.lexer.tokens.misc import LexicalGroupEnd
from thinglang.lexer.tokens.separator import LexicalSeparator
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.blocks.conditional import Conditional
from thinglang.parser.blocks.conditional_else import ConditionalElse
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.blocks.try_block import TryBlock
from thinglang.parser.blocks.handle_block import HandleBlock
from thinglang.parser.blocks.unconditional_else import UnconditionalElse
from thinglang.parser.definitions.member_definition import MemberDefinition
from thinglang.parser.definitions.method_definition import MethodDefinition
from thinglang.parser.definitions.thing_definition import ThingDefinition
from thinglang.parser.errors import VectorReductionError
from thinglang.parser.nodes import BaseNode
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.parser.statements.return_statement import ReturnStatement
from thinglang.parser.statements.throw_statement import ThrowStatement
from thinglang.parser.values.access import Access
from thinglang.parser.values.binary_operation import BinaryOperation

from thinglang.parser.values.inline_list import InlineList
from thinglang.parser.values.method_call import MethodCall
from thinglang.utils import collection_utils
from thinglang.utils.type_descriptors import ValueType, TypeList, ListType

"""
The primary component of the parser - describes token vectors and their reduction pipeline
"""

PARSING_ORDER = [  # Apply production rules in this order
    GenericIdentifier,

    ThingDefinition,
    MemberDefinition,
    MethodDefinition,

    Access,

    MethodCall,
    BinaryOperation,

    AssignmentOperation,
    ReturnStatement,
    ThrowStatement,

    Conditional,
    ConditionalElse,
    UnconditionalElse,

    Loop,

    TryBlock,
    HandleBlock
]


class TokenVector(object):
    """
    The base token vector
    """

    def __init__(self, tokens=None):
        self.tokens = tokens if tokens is not None else []

    def parse(self, expect_single=True) -> BaseNode:
        """
        Iteratively parses the token vector until a single node remains, or no further rule replacements can be made.
        """
        while self.perform_replacements():
            pass

        self.process_indentation()

        if not expect_single:
            return self.tokens

        if len(self.tokens) != 1 or not isinstance(self.tokens[0], (ValueType, BaseNode)):
            raise VectorReductionError('Could not reduce vector: {}'.format(self.tokens))

        if isinstance(self.tokens[0], TokenVector):
            return self.tokens[0].parse()

        return self.tokens[0]

    def perform_replacements(self):
        """
        Given a list of lexical tokens, attempt to find partial matches, in order, using the replacements list defined above.
        Whenever a match succeeds, the matching slice is spliced out of place, and replaced with a parsed token instance.
        The list is modified in place.
        :return: True if a replacement occurred, None otherwise
        """
        for target in PARSING_ORDER:
            match = target.propose_replacement(self.tokens)

            if not match:
                continue

            node, match_start, match_end = match

            token_slice = self.finalize_slice(match_start, match_end)
            self.tokens[match_start:match_end] = [node(*token_slice)]

            return True

    def finalize_slice(self, start, end):
        """
        Parses all nested vectors in a slice
        """
        return [token.parse() if isinstance(token, TokenVector) else token for token in self.tokens[start:end]]

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


class ParenthesesVector(TokenVector, ValueType, ListType):
    """
    Describes a vector of tokens bounded in parentheses, such as those in a method call's arguments or those
    signifying order-of-operations in an arithmetic operations
    """

    def parse(self, expect_single=False):
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


class BracketVector(ParenthesesVector, ValueType):
    """
    Describes a vector of tokens bounded in bracket, generally for creating in line lists.
    """

    def parse(self, expect_single=False):
        return InlineList(super().parse())


class ParameterVector(ParenthesesVector):
    """
    Describes a vector of type parameters, used for generic thing definitions
    """

    def parse(self, expect_single=False):
        return tuple([super().parse()])


class TypeVector(TokenVector, TypeList):
    """
    Describes a vector of type pairings, such as those describing method arguments (e.g. number value, text name)
    """

    def parse(self, expect_single=False):
        output = []

        self.tokens = super().parse(expect_single=False)

        if not all(isinstance(x, (Identifier, LexicalSeparator, ParameterVector)) for x in self.tokens):
            raise VectorReductionError('Only types, names and separators are allowed in a type vector', self.tokens)

        if len(self.tokens) < 2:
            raise VectorReductionError('Not enough items in a type vector')

        for components in collection_utils.chunks(self.tokens, 3):
            if len(components) < 2 or not isinstance(components[0], Identifier) or not isinstance(components[1], Identifier):
                raise VectorReductionError('Invalid syntax in type vector element - must be 2 consecutive names')

            if len(components) > 2 and not isinstance(components[2], LexicalSeparator):
                raise VectorReductionError('Expected separator, got {}'.format(components[1]))

            components[1].type = components[0]
            output.append(components[1])

        return output



