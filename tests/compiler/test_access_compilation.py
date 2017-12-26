from tests.compiler import compile_snippet, A_ID, LST_ID, SELF_ID, VAL1_ID, internal_call
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushMember, OpcodePushStatic


def test_local_list_immediate_index():
    assert compile_snippet('lst[123]') == [
        OpcodePushStatic(6),
        OpcodePushLocal(LST_ID),
        internal_call('list.get')
    ]


def test_local_list_non_immediate_index():
    assert compile_snippet('lst[a]') == [
        OpcodePushLocal(A_ID),
        OpcodePushLocal(LST_ID),
        internal_call('list.get')
    ]
    assert compile_snippet('lst[self.val1]') == [
        OpcodePushMember(SELF_ID, VAL1_ID),
        OpcodePushLocal(LST_ID),
        internal_call('list.get')
    ]

