import pytest

from thinglang.execution.errors import UnknownVariable, RedeclaredVariable
from thinglang import run


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
    with pytest.raises(UnknownVariable):
        run("""
thing Program
    setup

        if true
            number i = 10
            Output.write("inside after, i =", i)

        Output.write("outside after, i =", i)

    """)


@pytest.mark.skip(reason="Implement static analysis on AST")
def test_error_in_duplicate_assignment():
    with pytest.raises(RedeclaredVariable):
        run("""
thing Program
    setup
        number i = 0
        number i = 1
    """)