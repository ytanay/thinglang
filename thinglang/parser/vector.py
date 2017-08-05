import collections

from thinglang.lexer.tokens import LexicalGroupEnd
from thinglang.lexer.tokens.arithmetic import SecondOrderLexicalBinaryOperation, FirstOrderLexicalBinaryOperation, \
    LexicalNumericalValue
from thinglang.lexer.tokens.base import LexicalIdentifier, LexicalAccess, LexicalSeparator, LexicalIndent, \
    LexicalParenthesesOpen, LexicalParenthesesClose, LexicalAssignment
from thinglang.lexer.tokens.functions import LexicalDeclarationThing, LexicalDeclarationMember, \
    LexicalDeclarationConstructor, LexicalDeclarationMethod, LexicalDeclarationReturnType, LexicalArgumentListIndicator, \
    LexicalReturnStatement
from thinglang.lexer.tokens.logic import LexicalConditional, LexicalComparison, LexicalElse, LexicalRepeatWhile
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.base import InlineString, AssignmentOperation
from thinglang.parser.nodes.classes import ThingDefinition, MemberDefinition, MethodDefinition
from thinglang.parser.nodes.functions import Access, MethodCall, ArgumentList, ReturnStatement
from thinglang.parser.nodes.logic import Conditional, ConditionalElse, UnconditionalElse, Loop
from thinglang.utils import collection_utils
from thinglang.utils.type_descriptors import ValueType
from thinglang.utils.union_types import POTENTIALLY_RESOLVABLE


class TokenVector(object):

    def __init__(self, tokens=None):
        self.tokens = tokens if tokens is not None else []

    def parse(self):
        while self.perform_replacements():
            pass

        self.process_indentation()

        if len(self.tokens) != 1:
            raise ValueError('Could not reduce vector: {}'.format(self.tokens))

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
        return [token.parse() if isinstance(token, TokenVector) else token for token in token_slice]

    def process_indentation(self):
        """
        Converts a list of LEXICAL_INDENTATION tokens at the beginning of a parsed group into indentation value stored on the first real token.
        :param group:
        :return:
        """


        if not self.tokens:
            return

        if isinstance(self.tokens[-1], LexicalGroupEnd):
            self.tokens[-1:] = []


        if not isinstance(self.tokens[0], LexicalIndent):
            return

        iterable = iter(self.tokens)
        size = 0

        try:
            while isinstance(next(iterable), LexicalIndent):
                size += 1
        except StopIteration:
            pass

        self.tokens[0:size] = []

        if self.tokens:
            self.tokens[0].indent = size

    def append(self, token):
        self.tokens.append(token)

    def __str__(self):
        return '<{}>{}'.format(type(self).__name__, self.tokens)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, item):
        return self.tokens[item]

    def empty(self):
        return all(isinstance(x, (LexicalIndent, LexicalGroupEnd)) for x in self.tokens)


class ParenthesesVector(TokenVector, ValueType):

    def parse(self):
        if not self.tokens:
            return

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

    def parse(self):
        output = []

        if not all(isinstance(x, (LexicalIdentifier, LexicalSeparator)) for x in self.tokens):
            raise ValueError('Only types, names and separators are allowed in a type vector')

        if len(self.tokens) < 2:
            raise ValueError('Not enough items in a type vector')

        for components in collection_utils.chunks(self.tokens, 3):
            if len(components) < 2 or not isinstance(components[0], LexicalIdentifier) or not isinstance(components[1], LexicalIdentifier):
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


METHOD_ID = (LexicalIdentifier,) + tuple(ArithmeticOperation.OPERATIONS.keys())

PATTERNS = collections.OrderedDict([
    ((LexicalDeclarationThing, LexicalIdentifier), ThingDefinition),  # thing Program
    ((LexicalDeclarationMember, LexicalIdentifier, LexicalIdentifier), MemberDefinition),

    ((LexicalDeclarationMethod, METHOD_ID, TypeVector, LexicalDeclarationReturnType, LexicalIdentifier), MethodDefinition),  # does compute with number a
    ((LexicalDeclarationMethod, METHOD_ID, TypeVector), MethodDefinition),  # does compute with number a
    ((LexicalDeclarationMethod, METHOD_ID, LexicalDeclarationReturnType, LexicalIdentifier), MethodDefinition),  # does compute with number a
    ((LexicalDeclarationMethod, METHOD_ID), MethodDefinition),  # does say_hello

    ((LexicalDeclarationConstructor,), MethodDefinition),

    ((LexicalIdentifier, LexicalAccess, LexicalIdentifier), Access),  # person.name

    ((Access, ParenthesesVector), MethodCall),


    ((ValueType, SecondOrderLexicalBinaryOperation, ValueType), ArithmeticOperation),  # 4 * 2
    ((ValueType, FirstOrderLexicalBinaryOperation, ValueType), ArithmeticOperation),  # 4 + 2
    ((ValueType, LexicalComparison, ValueType), ArithmeticOperation),  # 4 == 2


    ((LexicalIdentifier, LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # number n = 1
    ((LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,
    ((Access, LexicalAssignment, ValueType), AssignmentOperation),  # n = 2,

    ((LexicalReturnStatement, ValueType), ReturnStatement),  # return 2
    ((LexicalReturnStatement,), ReturnStatement),

    ((LexicalConditional, ValueType), Conditional),  # if x
    ((LexicalElse, Conditional), ConditionalElse),
    ((LexicalElse,), UnconditionalElse),

    ((LexicalRepeatWhile, ValueType), Loop),  # repeat while
])
