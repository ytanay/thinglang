import pytest

from thinglang import pipeline
from thinglang.compiler.errors import DuplicateHandlerError
from thinglang.utils.source_context import SourceContext

DUPLICATE_EXCEPTION = """
thing Program
    
    try
        Console.print("Might throw")
    handle FirstException
        Console.print("Got exception")
    handle SecondException
        Console.print("Another exception")
    handle FirstException
        Console.print("Duplicate handler")
    
"""


def test_duplicate_exception_handlers():
    with pytest.raises(DuplicateHandlerError):
        pipeline.compile(SourceContext.wrap(DUPLICATE_EXCEPTION))