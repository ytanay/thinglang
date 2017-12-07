from tests.compiler import compile_local, A_ID, B_ID, SELF_ID, VAL1_ID, VAL2_ID, INST_ID, INNER_ID, INNER1_ID, \
    INNER2_ID, STATIC_START
from thinglang.compiler.opcodes import OpcodeAssignStatic, OpcodeAssignLocal, OpcodePushMember, OpcodePopLocal, \
    OpcodeDereference


def test_static_to_local():
    assert compile_local('a = 5') == [OpcodeAssignStatic(A_ID, STATIC_START)]
    assert compile_local('a = "hello"') == [OpcodeAssignStatic(A_ID, STATIC_START)]


def test_local_to_local():
    assert compile_local('a = b') == [OpcodeAssignLocal(A_ID, B_ID)]


def test_self_member_to_local():
    assert compile_local('a = self.val1') == [OpcodePushMember(SELF_ID, VAL1_ID), OpcodePopLocal(A_ID)]
    assert compile_local('b = self.val2') == [OpcodePushMember(SELF_ID, VAL2_ID), OpcodePopLocal(B_ID)]


def test_member_to_local():
    assert compile_local('a = inst.val1') == [OpcodePushMember(INST_ID, VAL1_ID), OpcodePopLocal(A_ID)]
    assert compile_local('b = inst.val2') == [OpcodePushMember(INST_ID, VAL2_ID), OpcodePopLocal(B_ID)]


def test_inner_self_member_to_local():
    assert compile_local('a = self.inner.inner1') == [OpcodePushMember(SELF_ID, INNER_ID), OpcodeDereference(INNER1_ID), OpcodePopLocal(A_ID)]
    assert compile_local('b = self.inner.inner2') == [OpcodePushMember(SELF_ID, INNER_ID), OpcodeDereference(INNER2_ID), OpcodePopLocal(B_ID)]


def test_inner_member_to_local():
    assert compile_local('a = inst.inner.inner1') == [OpcodePushMember(INST_ID, INNER_ID), OpcodeDereference(INNER1_ID), OpcodePopLocal(A_ID)]
    assert compile_local('b = inst.inner.inner2') == [OpcodePushMember(INST_ID, INNER_ID), OpcodeDereference(INNER2_ID), OpcodePopLocal(B_ID)]


