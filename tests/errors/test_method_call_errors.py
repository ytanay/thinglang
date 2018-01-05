import pytest

from thinglang import pipeline
from thinglang.compiler.errors import TargetNotCallable, NoMatchingOverload
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.inline_text import InlineString
from thinglang.lexer.values.numeric import NumericValue
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
    with pytest.raises(NoMatchingOverload) as e:
        pipeline.compile(SourceContext.wrap(BASE.format(code="self.no_args(1)")))

    assert e.value.methods[0].name == Identifier('no_args') and e.value.arguments == [NumericValue(1)]

    with pytest.raises(NoMatchingOverload) as e:
        pipeline.compile(SourceContext.wrap(BASE.format(code="self.two_args(1)")))

    assert e.value.methods[0].name == Identifier('two_args') and e.value.arguments == [NumericValue(1)]


def test_argument_type_mismatch():
    with pytest.raises(NoMatchingOverload) as e:
        pipeline.compile(SourceContext.wrap(BASE.format(code='self.two_args("hello", 3)')))

    assert e.value.methods[0].name == Identifier('two_args') and e.value.arguments == [InlineString("hello"), NumericValue(3)]

    pipeline.compile(SourceContext.wrap(BASE.format(code='self.two_args(3, 3)')))  # Can be implicitly casted

