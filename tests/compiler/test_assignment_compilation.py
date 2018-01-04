from tests.compiler import compile_snippet, A_ID, B_ID, SELF_ID, VAL1_ID, VAL2_ID, INST_ID, INNER_ID, INNER1_ID, \
    INNER2_ID, STATIC_START, internal_call, LST_ID, CONTAINER
from thinglang.compiler.opcodes import OpcodeAssignStatic, OpcodeAssignLocal, OpcodePushMember, OpcodePopLocal, \
    OpcodeDereference, OpcodePushStatic, OpcodePushLocal, OpcodeCallStatic, OpcodePopDereferenced


def test_static_to_local():
    assert compile_snippet('a = 5') == [OpcodeAssignStatic(A_ID, STATIC_START)]
    assert compile_snippet('a = "hello"') == [OpcodePushStatic(STATIC_START), internal_call('text.as number'), OpcodePopLocal(A_ID)]


def test_local_to_local():
    assert compile_snippet('a = b') == [OpcodeAssignLocal(A_ID, B_ID)]


def test_self_member_to_local():
    assert compile_snippet('a = self.val1') == [OpcodePushMember(SELF_ID, VAL1_ID), OpcodePopLocal(A_ID)]
    assert compile_snippet('b = self.val2') == [OpcodePushMember(SELF_ID, VAL2_ID), OpcodePopLocal(B_ID)]


def test_member_to_local():
    assert compile_snippet('a = inst.val1') == [OpcodePushMember(INST_ID, VAL1_ID), OpcodePopLocal(A_ID)]
    assert compile_snippet('b = inst.val2') == [OpcodePushMember(INST_ID, VAL2_ID), OpcodePopLocal(B_ID)]


def test_inner_self_member_to_local():
    assert compile_snippet('a = self.inner.inner1') == [OpcodePushMember(SELF_ID, INNER_ID), OpcodeDereference(INNER1_ID), OpcodePopLocal(A_ID)]
    assert compile_snippet('b = self.inner.inner2') == [OpcodePushMember(SELF_ID, INNER_ID), OpcodeDereference(INNER2_ID), OpcodePopLocal(B_ID)]


def test_inner_member_to_local():
    assert compile_snippet('a = inst.inner.inner1') == [OpcodePushMember(INST_ID, INNER_ID), OpcodeDereference(INNER1_ID), OpcodePopLocal(A_ID)]
    assert compile_snippet('b = inst.inner.inner2') == [OpcodePushMember(INST_ID, INNER_ID), OpcodeDereference(INNER2_ID), OpcodePopLocal(B_ID)]


def test_static_to_indexed():
    assert compile_snippet('lst[0] = Container()') == [
        OpcodePushStatic(STATIC_START),  # Push index 0
        OpcodeCallStatic(CONTAINER, 0),  # Push constant 5
        OpcodePushLocal(LST_ID),  # Push the list
        internal_call('list.set')
    ]


def test_static_to_member_of_indexed():
    assert compile_snippet('lst[0].inner1 = 5') == [
        OpcodePushStatic(STATIC_START),  # Push index 0
        OpcodePushStatic(STATIC_START + 1),  # Push constant 5
        OpcodePushLocal(LST_ID),  # Push the list
        internal_call('list.get'),
        OpcodePopDereferenced(INNER1_ID)
    ]
