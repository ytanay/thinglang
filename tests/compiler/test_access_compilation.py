from tests.compiler import compile_local, A_ID, LST_ID, SELF_ID, VAL1_ID, LIST_GET
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushMember, OpcodePushStatic


def test_local_list_immediate_index():
    assert compile_local('lst[123]') == [
        OpcodePushLocal(LST_ID),
        OpcodePushStatic(5),
        LIST_GET
    ]


def test_local_list_non_immediate_index():
    assert compile_local('lst[a]') == [
        OpcodePushLocal(LST_ID),
        OpcodePushLocal(A_ID),
        LIST_GET
    ]
    assert compile_local('lst[self.val1]') == [
        OpcodePushLocal(LST_ID),
        OpcodePushMember(SELF_ID, VAL1_ID),
        LIST_GET
    ]

