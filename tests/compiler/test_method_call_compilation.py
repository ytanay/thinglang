from tests.compiler import compile_local, SELF_ID, LST_ID, VAL1_ID, LIST_GET
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushMember, OpcodeCall, OpcodePushStatic


def test_access_in_method_args():
    assert compile_local('self.action(lst[123])') == [
        OpcodePushLocal(SELF_ID),
        OpcodePushLocal(LST_ID),
        OpcodePushStatic(5),
        LIST_GET,
        OpcodeCall(0, 1)
    ]

    assert compile_local('self.action(lst[self.val1])') == [
        OpcodePushLocal(SELF_ID),
        OpcodePushLocal(LST_ID),
        OpcodePushMember(SELF_ID, VAL1_ID),
        LIST_GET,
        OpcodeCall(0, 1)
    ]
