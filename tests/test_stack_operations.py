import pytest

from thinglang.execution.errors import UnresolvedReference, DuplicateDeclaration
from thinglang import run

"""
These may be redundant with static analysis
"""


def test_stack_resolution_in_block():
    assert run("""
thing Program
    setup
        number i = 0
        Output.write("outside before, i =", i)
        if true
            Output.write("inside before, i =", i)
            i = 10
            Output.write("inside after, i =", i)

        Output.write("outside after, i =", i)

    """).output == """
outside before, i = 0
inside before, i = 0
inside after, i = 10
outside after, i = 10""".strip()


def test_stack_resolution_error_during_access_after_nested_deceleration():
    with pytest.raises(UnresolvedReference):
        run("""
thing Program
    setup

        if true
            number i = 10
            Output.write("inside after, i =", i)

        Output.write("outside after, i =", i)

    """)
