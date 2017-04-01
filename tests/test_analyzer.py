import pytest

from thinglang import run
from thinglang.execution.errors import ReturnInConstructorError, EmptyMethodBody, EmptyThingDefinition, \
    ArgumentCountMismatch


def test_return_in_constructor():
    with pytest.raises(ReturnInConstructorError):
        run("""
thing Program
    setup
        return 10
    """)


def test_empty_method_body():
    with pytest.raises(EmptyMethodBody):
        run("""
thing Program
    setup
    does start
    """)


def test_empty_thing_definition():
    with pytest.raises(EmptyThingDefinition):
        run("""
thing Program
    """)
