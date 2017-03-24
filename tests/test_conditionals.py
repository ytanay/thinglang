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

    """).output == """dog is dog"""


def test_boolean_constant():
    assert run("""
thing Program
    does start
        if true
            Output.write("true is truthy")

        if false
            Output.write("false is truthy")

    """).output == """true is truthy"""


def test_unconditional_else():
    assert run("""
thing Program
    does start
        if "dog" eq "dog"
            Output.write("dog is dog")
        otherwise
            Output.write("dog is not dog")

        if "dog" eq "cat"
            Output.write("dog is cat")
        otherwise
            Output.write("dog is not cat")
    """).output == """dog is dog\ndog is not cat"""


def test_conditional_else():
    assert run("""
thing Program
    does start
        if "dog" eq "cat"
            Output.write("dog is cat")
        otherwise if "dog" eq "dog"
            Output.write("dog is dog")
        otherwise if "dog" eq "dog"
            Output.write("dog is still dog")
        otherwise
            Output.write("dog is not dog and not cat")

        if "dog" eq "cat"
            Output.write("dog is cat")
        otherwise if "dog" eq "Dog"
            Output.write("dog is Dog")
        otherwise if "dog" eq "mouse"
            Output.write("dog is mouse")
        otherwise
            Output.write("dog is not cat and not mouse and not Dog")
    """).output == """dog is dog\ndog is not cat and not mouse and not Dog"""
