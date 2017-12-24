from tests.compiler import compile_snippet, SELF_ID, LST_ID, VAL1_ID, internal_call
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushMember, OpcodeCall, OpcodePushStatic


def test_access_in_method_args():
    assert compile_snippet('self.action(lst[123])') == [
        OpcodePushLocal(SELF_ID),
        OpcodePushLocal(LST_ID),
        OpcodePushStatic(6),
        internal_call('list.get'),
        OpcodeCall(0, 1)
    ]

    assert compile_snippet('self.action(lst[self.val1])') == [
        OpcodePushLocal(SELF_ID),
        OpcodePushLocal(LST_ID),
        OpcodePushMember(SELF_ID, VAL1_ID),
        internal_call('list.get'),
        OpcodeCall(0, 1)
    ]
