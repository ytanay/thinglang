from tests.compiler import compile_snippet, A_ID, LST_ID, SELF_ID, VAL1_ID, internal_call, A_INST, INNER_ID, \
    CONTAINER_INNER_ID
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushMember, OpcodePushStatic, OpcodePop, \
    OpcodeDereference, OpcodeCallVirtual


def test_direct_member_access():
    assert compile_snippet('a_inst.a1') == [
        OpcodePushMember(A_INST, 0)
    ]


def test_nested_member_access():
    assert compile_snippet('self.inner.inner.inner') == [
        OpcodePushMember(SELF_ID, INNER_ID),
        OpcodeDereference(CONTAINER_INNER_ID),
        OpcodeDereference(CONTAINER_INNER_ID)
    ]


def test_member_access_via_method_call():
    assert compile_snippet('a_inst.me().a1') == [
        OpcodePushLocal(A_INST),
        OpcodeCallVirtual(1),
        OpcodeDereference(0)
    ]

    assert compile_snippet('a_inst.me().me().a1') == [
        OpcodePushLocal(A_INST),
        OpcodeCallVirtual(1),
        OpcodeCallVirtual(1),
        OpcodeDereference(0)
    ]


def test_local_list_immediate_index():
    assert compile_snippet('lst[123]') == [
        OpcodePushStatic(6),
        OpcodePushLocal(LST_ID),
        internal_call('list.get'),
        OpcodePop()
    ]


def test_local_list_non_immediate_index():
    assert compile_snippet('lst[a]') == [
        OpcodePushLocal(A_ID),
        OpcodePushLocal(LST_ID),
        internal_call('list.get'),
        OpcodePop()
    ]
    assert compile_snippet('lst[self.val1]') == [
        OpcodePushMember(SELF_ID, VAL1_ID),
        OpcodePushLocal(LST_ID),
        internal_call('list.get'),
        OpcodePop()
    ]


