from tests.compiler import compile_snippet, SELF_ID, LST_ID, VAL1_ID, internal_call
from thinglang.compiler.opcodes import OpcodePushLocal, OpcodePushMember, OpcodeCall, OpcodePushStatic, \
    OpcodeCallVirtual


def test_access_in_method_args():
    assert compile_snippet('self.action(lst[123])') == [
        OpcodePushStatic(6),
        OpcodePushLocal(LST_ID),
        internal_call('list.get'),
        OpcodePushLocal(SELF_ID),
        OpcodeCallVirtual(1)
    ]

    assert compile_snippet('self.action(lst[self.val1])') == [
        OpcodePushMember(SELF_ID, VAL1_ID),
        OpcodePushLocal(LST_ID),
        internal_call('list.get'),
        OpcodePushLocal(SELF_ID),
        OpcodeCallVirtual(1)
    ]
