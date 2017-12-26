import pytest

from tests.compiler import compile_snippet, A_INST, B_INST, A_THING, B_THING, compile_template
from thinglang.compiler.errors import InvalidReference
from thinglang.compiler.opcodes import OpcodePushMember, OpcodeInstantiate, OpcodeReturn, OpcodePushLocal, \
    OpcodePopMember


def test_regular_inheritance_member_access():
    assert compile_snippet('a_inst.a1') == [
        OpcodePushMember(A_INST, 0)
    ]

    assert compile_snippet('b_inst.b1') == [
        OpcodePushMember(B_INST, 1)
    ]

    assert compile_snippet('b_inst.a1') == [
        OpcodePushMember(B_INST, 0)
    ]


def test_regular_inheritance_invalid_member_access():
    with pytest.raises(InvalidReference):
        compile_snippet('a_inst.b1')

    with pytest.raises(InvalidReference):
        compile_snippet('b_inst.c1')


def test_constructor_compilation():
    assert compile_template(thing_id=A_THING) == [
        OpcodeInstantiate(0, 1),  # Implicit constructor (0-arg), 1 member
        OpcodeReturn()
    ]

    assert compile_template(thing_id=B_THING) == [
        OpcodeInstantiate(1, 2),  # Explicit constructor (1-arg), 1 member +
        OpcodePushLocal(1),  # Push the first argument
        OpcodePopMember(0, 1),  # Set it as the second member of self
        OpcodeReturn()
    ]
