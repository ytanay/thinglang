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

