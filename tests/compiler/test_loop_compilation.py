from tests.compiler import compile_local, LST_ID, IMPLICIT_ITERATOR_ID, IMPLICIT_ITERATION_ID, internal_call
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePopLocal, OpcodeJumpConditional, \
    OpcodeJump


def test_access_in_method_args():

    assert compile_local('for number x in lst') == [
        OpcodePushLocal(LST_ID),

        internal_call('list.iterator'),  # Create iterator
        OpcodePopLocal(IMPLICIT_ITERATOR_ID),  # Insert it into the frame

        OpcodePushLocal(IMPLICIT_ITERATOR_ID),  # TODO: is this optimal?
        internal_call('iterator.has_next'),
        OpcodeJumpConditional(23),  # Jump outside if not

        OpcodePushLocal(IMPLICIT_ITERATOR_ID),
        internal_call('iterator.next'),  # Call next
        OpcodePopLocal(IMPLICIT_ITERATION_ID),  # Insert into frame

        OpcodeJump(16)

    ]

