import collections

from thinglang.lexer.tokens.arithmetic import SecondOrderLexicalBinaryOperation, FirstOrderLexicalBinaryOperation, \
    LexicalNumericalValue
from thinglang.lexer.tokens.base import LexicalIdentifier, LexicalAccess, LexicalSeparator
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.base import InlineString
from thinglang.parser.nodes.functions import Access, MethodCall, ArgumentList
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
        return '<TV>{}'.format(self.tokens)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, item):
        return self.tokens[item]


class ParenthesesVector(TokenVector):

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

VALUE_TYPES = LexicalIdentifier, LexicalNumericalValue, InlineString, ParenthesesVector

PATTERNS = collections.OrderedDict([
    ((LexicalIdentifier, LexicalAccess, LexicalIdentifier), Access),  # person.name
    ((Access, ParenthesesVector), MethodCall),
    ((VALUE_TYPES, SecondOrderLexicalBinaryOperation, VALUE_TYPES), ArithmeticOperation),  # 4 * 2
    ((VALUE_TYPES, FirstOrderLexicalBinaryOperation, VALUE_TYPES), ArithmeticOperation),  # 4 + 2
])
