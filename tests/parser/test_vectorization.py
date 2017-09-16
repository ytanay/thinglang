import pytest

from tests.infrastructure.test_utils import validate_types, lexer_single
from thinglang.lexer.tokens.arithmetic import NumericValue, LexicalMultiplication, LexicalAddition
from thinglang.lexer.tokens.base import LexicalIdentifier, LexicalAccess, LexicalSeparator
from thinglang.parser import parser
from thinglang.parser.values.inline_text import InlineString
from thinglang.parser.vector import TokenVector


def test_simple_vectorization():
    tokens = lexer_single('person.walk("a", 1)')
    vector = parser.collect_vectors(tokens)

    validate_types(vector, [
        LexicalIdentifier,
        LexicalAccess,
        LexicalIdentifier, [
            InlineString,
            LexicalSeparator,
            NumericValue
        ]
    ], TokenVector)


def test_complex_vectorization():
    tokens = lexer_single('person.walk(8 * (1 + 3), location.random(2 * (4 + 9)))')
    vector = parser.collect_vectors(tokens)

    validate_types(vector, [
        LexicalIdentifier,
        LexicalAccess,
        LexicalIdentifier, [
            NumericValue,
            LexicalMultiplication,
            [
                NumericValue,
                LexicalAddition,
                NumericValue
            ],
            LexicalSeparator,
            LexicalIdentifier,
            LexicalAccess,
            LexicalIdentifier,
            [
                NumericValue,
                LexicalMultiplication,
                [
                    NumericValue,
                    LexicalAddition,
                    NumericValue
                ]
            ]

        ]
    ], TokenVector)


def test_missing_closing_token():
    tokens = lexer_single('(5 * (2 + 3)')
    with pytest.raises(ValueError):
        parser.collect_vectors(tokens)


def test_extraneous_closing_tokens():
    tokens = lexer_single('(5 * (2 + 3)))')
    with pytest.raises(ValueError):
        parser.collect_vectors(tokens)
