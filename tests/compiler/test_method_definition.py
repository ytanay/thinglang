import pytest

from tests.compiler import compile_base, internal_call
from thinglang.compiler.errors import SelfInStaticMethod
from thinglang.compiler.opcodes import OpcodePushStatic, OpcodePushLocal

SELF_USE_IN_STATIC_METHOD = '''
thing Program
    has number n1
     
    static does something
        {}
        
'''


def test_direct_self_use_in_static_function():
    with pytest.raises(SelfInStaticMethod):
        compile_base(SELF_USE_IN_STATIC_METHOD.format('return self'))

    with pytest.raises(SelfInStaticMethod):
        compile_base(SELF_USE_IN_STATIC_METHOD.format('Console.print(self)'))


def test_self_dereference_in_static_function():
    with pytest.raises(SelfInStaticMethod):
        compile_base(SELF_USE_IN_STATIC_METHOD.format('self.n1'))


