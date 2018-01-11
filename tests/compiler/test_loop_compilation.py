from tests.compiler import compile_snippet, LST_ID, IMPLICIT_ITERATOR_ID, IMPLICIT_ITERATION_ID, internal_call, \
    STATIC_START
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePopLocal, OpcodeJumpConditional, \
    OpcodeJump, OpcodePushStatic


def test_iteration_loop():

    assert compile_snippet('for Container x in lst') == [
        OpcodePushLocal(LST_ID),

        internal_call('list.iterator'),  # Create iterator
        OpcodePopLocal(IMPLICIT_ITERATOR_ID),  # Insert it into the frame

        OpcodePushLocal(IMPLICIT_ITERATOR_ID),  # TODO: is this optimal?
        internal_call('iterator.has_next'),
        OpcodeJumpConditional(30),  # Jump outside if not

        OpcodePushLocal(IMPLICIT_ITERATOR_ID),
        internal_call('iterator.next'),  # Call next
        OpcodePopLocal(IMPLICIT_ITERATION_ID),  # Insert into frame

        OpcodeJump(23)

    ]


def test_simple_break():
    assert compile_snippet({'while true': ['Console.write("")', 'break', 'Console.write("")']}) == [
        OpcodePushStatic(STATIC_START),
        OpcodeJumpConditional(28),
        OpcodePushStatic(STATIC_START + 1),
        internal_call('Console.write'),
        OpcodeJump(28), # TODO: optimize case where `if something: break`
        OpcodePushStatic(STATIC_START + 2),
        internal_call('Console.write'),
        OpcodeJump(20)
    ]


def test_simple_continue():
    assert compile_snippet({'while true': ['Console.write("")', 'continue', 'Console.write("")']}) == [
        OpcodePushStatic(STATIC_START),
        OpcodeJumpConditional(28),
        OpcodePushStatic(STATIC_START + 1),
        internal_call('Console.write'),
        OpcodeJump(20),
        OpcodePushStatic(STATIC_START + 2),
        internal_call('Console.write'),
        OpcodeJump(20)
    ]
