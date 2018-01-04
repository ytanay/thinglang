import pytest

from tests.compiler import compile_snippet, internal_call,  STATIC_START, LOCAL_START
from thinglang.compiler.errors import NoMatchingOverload, InvalidReference
from thinglang.compiler.opcodes import OpcodePopLocal, OpcodePushStatic


def test_inline_list_compilation():

    assert compile_snippet('list<number> numbers = [1, 2, 3]') == [
        OpcodePushStatic(STATIC_START),  # Push the values
        OpcodePushStatic(STATIC_START + 1),
        OpcodePushStatic(STATIC_START + 2),

        internal_call('list.__constructor__'),  # Create the list

        internal_call('list.append'),  # Compile 3 append calls
        internal_call('list.append'),
        internal_call('list.append'),

        OpcodePopLocal(LOCAL_START)
    ]


def test_inline_list_type_homogeneity():
    with pytest.raises(NoMatchingOverload):
        assert compile_snippet('list<number> numbers = [1, Container(), 3]')


def test_inline_list_declaration_type_match():
    with pytest.raises(InvalidReference):
        assert compile_snippet('list<number> numbers = [Container(), Container(), Container()]')


