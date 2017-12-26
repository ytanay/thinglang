import pytest

from tests.compiler import compile_base, internal_call
from thinglang.compiler.opcodes import OpcodePushStatic, OpcodePushLocal

INLINING_TEST_PROGRAM = '''
thing Program
    setup
        number n1 = 0
        number n2 = 1
        {}
    
    static does add with number a, number b
        a + b
        
    static does external_call with text file_name
        File(file_name)
    
'''


# TODO: test tracking

def test_inlining_binary_op_constants():
    assert compile_base(INLINING_TEST_PROGRAM.format('self.add(1, 2)'), trim=2) == [
        OpcodePushStatic(2),
        OpcodePushStatic(3),
        internal_call('number.__addition__')
    ]


def test_inlining_binary_op_variables():
    assert compile_base(INLINING_TEST_PROGRAM.format('self.add(n1, n2)'), trim=2) == [
        OpcodePushLocal(1),
        OpcodePushLocal(2),
        internal_call('number.__addition__')
    ]


def test_inlining_binary_op_mixed():
    assert compile_base(INLINING_TEST_PROGRAM.format('self.add(2, n1)'), trim=2) == [
        OpcodePushStatic(2),
        OpcodePushLocal(1),
        internal_call('number.__addition__')
    ]


def test_inlining_second_call_simple():
    assert compile_base(INLINING_TEST_PROGRAM.format('self.external_call("Hello")'), trim=2) == [
        OpcodePushStatic(2),
        internal_call('File.__constructor__')
    ]


@pytest.mark.skip
def test_inlining_internal_call():
    print(internal_call('Console.write'))
    print(compile_base(INLINING_TEST_PROGRAM.format('Console.print("Hello")'), trim=2))