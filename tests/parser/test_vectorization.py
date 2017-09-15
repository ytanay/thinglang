import pytest

from tests.infrastructure.test_utils import validate_types, lexer_single
from thinglang import parser
from thinglang.lexer import lexer
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue, LexicalMultiplication, LexicalAddition
from thinglang.lexer.tokens.base import LexicalIdentifier, LexicalAccess, LexicalSeparator
from thinglang.parser import TokenVector
from thinglang.parser.nodes.values.inline_text import InlineString


def test_simple_vectorization():
    tokens = lexer_single('person.walk("a", 1)')
    vector = parser.collect_vectors(tokens)

    validate_types(vector, [
        LexicalIdentifier,
        LexicalAccess,
        LexicalIdentifier, [
            InlineString,
            LexicalSeparator,
            LexicalNumericalValue
        ]
    ], TokenVector)


def test_complex_vectorization():
    tokens = lexer_single('person.walk(8 * (1 + 3), location.random(2 * (4 + 9)))')
    vector = parser.collect_vectors(tokens)

    validate_types(vector, [
        LexicalIdentifier,
        LexicalAccess,
        LexicalIdentifier, [
            LexicalNumericalValue,
            LexicalMultiplication,
            [
                LexicalNumericalValue,
                LexicalAddition,
                LexicalNumericalValue
            ],
            LexicalSeparator,
            LexicalIdentifier,
            LexicalAccess,
            LexicalIdentifier,
            [
                LexicalNumericalValue,
                LexicalMultiplication,
                [
                    LexicalNumericalValue,
                    LexicalAddition,
                    LexicalNumericalValue
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

