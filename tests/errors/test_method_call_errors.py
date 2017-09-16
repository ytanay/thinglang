import pytest

from thinglang import pipeline
from thinglang.compiler.errors import TargetNotCallable, ArgumentCountMismatch, ArgumentTypeMismatch
from thinglang.lexer.values.identifier import Identifier
from thinglang.utils.source_context import SourceContext

BASE = """
thing Program
    has number member1
    setup
        {code}
        
    does no_args
        1 + 1
        
    does two_args with number a, text b
        1 + 1
"""


def test_method_call_on_non_method_target():
    with pytest.raises(TargetNotCallable):
        pipeline.compile(SourceContext.wrap(BASE.format(code="self.member1()")))


def test_argument_count_mismatch():
    with pytest.raises(ArgumentCountMismatch) as e:
        pipeline.compile(SourceContext.wrap(BASE.format(code="self.no_args(1)")))

    assert e.value.expected_count == 0 and e.value.actual_count == 1

    with pytest.raises(ArgumentCountMismatch) as e:
        pipeline.compile(SourceContext.wrap(BASE.format(code="self.two_args(1)")))

    assert e.value.expected_count == 2 and e.value.actual_count == 1


def test_argument_type_mismatch():
    with pytest.raises(ArgumentTypeMismatch) as e:
        pipeline.compile(SourceContext.wrap(BASE.format(code='self.two_args("hello", 3)')))

    assert e.value.index == 0 and e.value.expected_type == Identifier("number") and e.value.actual_type == Identifier("text")

    with pytest.raises(ArgumentTypeMismatch) as e:
        pipeline.compile(SourceContext.wrap(BASE.format(code='self.two_args(3, 3)')))

    assert e.value.index == 1 and e.value.actual_type == Identifier("number") and e.value.expected_type == Identifier("text")

