from tests.compiler import compile_local, LST_ID, IMPLICIT_ITERATOR_ID, IMPLICIT_ITERATION_ID
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodeCallInternal, OpcodePopLocal, OpcodeJumpConditional, \
    OpcodeJump
from thinglang.foundation.definitions import INTERNAL_TYPE_ORDERING
from thinglang.lexer.values.identifier import Identifier


def test_access_in_method_args():
    assert compile_local('for number x in lst') == [
        OpcodePushLocal(LST_ID),
        OpcodeCallInternal(INTERNAL_TYPE_ORDERING[Identifier("list")], 4),  # Create iterator
        OpcodePopLocal(IMPLICIT_ITERATOR_ID),  # Insert it into the frame

        OpcodePushLocal(IMPLICIT_ITERATOR_ID),  # TODO: is this optimal?
        OpcodeCallInternal(INTERNAL_TYPE_ORDERING[Identifier('iterator')], 1),  # Call has_next
        OpcodeJumpConditional(23),  # Jump outside if not

        OpcodePushLocal(IMPLICIT_ITERATOR_ID),
        OpcodeCallInternal(INTERNAL_TYPE_ORDERING[Identifier('iterator')], 2),  # Call next
        OpcodePopLocal(IMPLICIT_ITERATION_ID),  # Insert into frame

        OpcodeJump(16)

    ]

