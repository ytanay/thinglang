import pytest

from thinglang.compiler.opcodes import OpcodePass, OpcodePushMember


ARGUMENT_COUNT = (ValueError, OpcodePushMember()), (ValueError, OpcodePass(1, 2))
TYPE_MISMATCH = (TypeError, OpcodePushMember('a', 2)),


@pytest.mark.parametrize('test_case', ARGUMENT_COUNT + TYPE_MISMATCH, ids=lambda x: 'opcode={},error={}'.format(x[1], x[0]))
def test_opcode_resolution(test_case):
    expected_error, opcode = test_case

    with pytest.raises(expected_error):
        opcode.resolve()
