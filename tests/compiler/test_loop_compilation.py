from tests.compiler import compile_snippet, LST_ID, IMPLICIT_ITERATOR_ID, IMPLICIT_ITERATION_ID, internal_call
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePopLocal, OpcodeJumpConditional, \
    OpcodeJump


def test_iteration_loop():

    assert compile_snippet('for number x in lst') == [
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

