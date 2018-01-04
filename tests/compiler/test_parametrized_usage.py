import pytest

from tests.compiler import compile_snippet
from thinglang.compiler.errors import UnfilledGenericParameters


def test_both_parameters_unfilled():
    with pytest.raises(UnfilledGenericParameters):
        compile_snippet('list my_lst = list()')


def test_right_parameter_unfilled():
    with pytest.raises(UnfilledGenericParameters):
        compile_snippet('list<Container> my_lst = list()')


def test_left_parameter_unfilled():
    with pytest.raises(UnfilledGenericParameters):
        compile_snippet('list my_lst = list<Container>()')


def test_valid_static_usage():
    compile_snippet('Generic.static_method()')


def test_invalid_instance_usage():
    with pytest.raises(UnfilledGenericParameters):
        compile_snippet('Generic().instance_method()')
