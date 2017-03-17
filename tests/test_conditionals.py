import pytest

from thinglang.runner import run


def test_simple_conditionals():
    assert run("""
thing Program
    does start
        if "dog" eq "dog"
            Output.write("dog is dog")
        if "dog" eq "cat"
            Output.write("dog is cat")
    """).output == """dog is dog""".strip()
