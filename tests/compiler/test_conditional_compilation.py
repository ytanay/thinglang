from tests.compiler import compile_snippet, STATIC_START, internal_call
from thinglang.compiler.opcodes import OpcodePushStatic, OpcodeJumpConditional, OpcodeJump

PREFIX = [
    OpcodePushStatic(STATIC_START),
    OpcodePushStatic(STATIC_START + 1),
    internal_call('text.__equals__'),
]

def test_simple_conditional():
    assert compile_snippet({'if "dog" == "dog"': ['Console.write("executing")']}) == PREFIX + [
        OpcodeJumpConditional(26),
        OpcodePushStatic(STATIC_START + 2),
        internal_call('Console.write')
    ]


def test_empty_conditional():
    assert compile_snippet({'if "dog" == "dog"': ['pass']}) == PREFIX + [
        OpcodeJumpConditional(24)
    ]

