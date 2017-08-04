from typing import List, Any

import pytest

from thinglang import parser
from thinglang.lexer import lexer
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue, LexicalMultiplication, LexicalAddition
from thinglang.lexer.tokens.base import LexicalIdentifier, LexicalAccess, LexicalSeparator
from thinglang.parser import TokenVector
from thinglang.parser.nodes.base import InlineString


def validate_vector_types(vector: TokenVector, types: List[Any]) -> None:
    assert len(vector) == len(types)

    for elem, expected_type in zip(vector, types):
        if isinstance(elem, TokenVector) and isinstance(expected_type, list):
            validate_vector_types(elem, expected_type)
        else:
            assert elem.implements(expected_type)


def test_simple_vectorization():
    tokens = lexer.lexer_single('person.walk("a", 1)')
    vector = parser.collect_vectors(tokens)

    validate_vector_types(vector, [
        LexicalIdentifier,
        LexicalAccess,
        LexicalIdentifier, [
            InlineString,
            LexicalSeparator,
            LexicalNumericalValue
        ]
    ])


def test_complex_vectorization():
    tokens = lexer.lexer_single('person.walk(8 * (1 + 3), location.random(2 * (4 + 9)))')
    vector = parser.collect_vectors(tokens)

    validate_vector_types(vector, [
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
    ])


def test_missing_closing_token():
    tokens = lexer.lexer_single('(5 * (2 + 3)')
    with pytest.raises(ValueError):
        parser.collect_vectors(tokens)


def test_extraneous_closing_tokens():
    tokens = lexer.lexer_single('(5 * (2 + 3)))')
    with pytest.raises(ValueError):
        parser.collect_vectors(tokens)

