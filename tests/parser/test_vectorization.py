import pytest

from tests.infrastructure.test_utils import validate_types, lexer_single
from thinglang.lexer.operators.binary import LexicalAddition, LexicalMultiplication
from thinglang.lexer.tokens.access import LexicalAccess
from thinglang.lexer.tokens.separator import LexicalSeparator
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser import parser
from thinglang.lexer.values.inline_text import InlineString
from thinglang.parser.vector import TokenVector


def test_simple_vectorization():
    tokens = lexer_single('person.walk("a", 1)')
    vector = parser.collect_vectors(tokens)

    validate_types(vector, [
        Identifier,
        LexicalAccess,
        Identifier, [
            InlineString,
            LexicalSeparator,
            NumericValue
        ]
    ], TokenVector)


def test_complex_vectorization():
    tokens = lexer_single('person.walk(8 * (1 + 3), location.random(2 * (4 + 9)))')
    vector = parser.collect_vectors(tokens)

    validate_types(vector, [
        Identifier,
        LexicalAccess,
        Identifier, [
            NumericValue,
            LexicalMultiplication,
            [
                NumericValue,
                LexicalAddition,
                NumericValue
            ],
            LexicalSeparator,
            Identifier,
            LexicalAccess,
            Identifier,
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


@pytest.mark.parametrize('source', ['(5 * (2 + 3)', '[[1, 2, 3]'])
def test_missing_closing_token(source):
    tokens = lexer_single(source)
    with pytest.raises(ValueError):
        parser.collect_vectors(tokens)


@pytest.mark.parametrize('source', ['(5 * (2 + 3)))', '[[1, 2, 3]]]'])
def test_extraneous_closing_tokens(source):
    tokens = lexer_single(source)
    with pytest.raises(ValueError):
        parser.collect_vectors(tokens)
