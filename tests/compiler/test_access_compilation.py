from tests.compiler import compile_local, A_ID, LST_ID, SELF_ID, VAL1_ID, internal_call
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushMember, OpcodePushStatic


def test_local_list_immediate_index():
    assert compile_local('lst[123]') == [
        OpcodePushLocal(LST_ID),
        OpcodePushStatic(5),
        internal_call('list.get')
    ]


def test_local_list_non_immediate_index():
    assert compile_local('lst[a]') == [
        OpcodePushLocal(LST_ID),
        OpcodePushLocal(A_ID),
        internal_call('list.get')
    ]
    assert compile_local('lst[self.val1]') == [
        OpcodePushLocal(LST_ID),
        OpcodePushMember(SELF_ID, VAL1_ID),
        internal_call('list.get')
    ]

