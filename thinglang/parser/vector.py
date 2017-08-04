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


VALUE_TYPES = LexicalIdentifier, LexicalNumericalValue, InlineString, ParenthesesVector

PATTERNS = collections.OrderedDict([
    ((LexicalIdentifier, LexicalAccess, LexicalIdentifier), Access),  # person.name
    ((Access, ParenthesesVector), MethodCall),
    ((VALUE_TYPES, SecondOrderLexicalBinaryOperation, VALUE_TYPES), ArithmeticOperation),  # 4 * 2
    ((VALUE_TYPES, FirstOrderLexicalBinaryOperation, VALUE_TYPES), ArithmeticOperation),  # 4 + 2
])
