import pytest

from thinglang import pipeline
from thinglang.compiler.errors import DuplicateHandlerError, ExceptionSpecificityError
from thinglang.utils.source_context import SourceContext

DUPLICATE_EXCEPTION = """
try
    Console.print("Might throw")
handle FirstException
    Console.print("Got exception")
handle SecondException
    Console.print("Another exception")
handle FirstException
    Console.print("Duplicate handler")
    
"""


SPECIFICITY_EXCEPTION = """
thing Exception1 extends Exception
thing Exception2 extends Exception1

thing Program
    setup   
        try
            Console.print("Might throw")
        handle Exception1
            Console.print("Got exception")
        handle Exception2
            Console.print("Another exception")
        
"""


def test_duplicate_exception_handlers():
    with pytest.raises(DuplicateHandlerError):
        pipeline.compile(SourceContext.wrap(DUPLICATE_EXCEPTION))


def test_invalid_specificity_exception_handlers():
    with pytest.raises(ExceptionSpecificityError):
        pipeline.compile(SourceContext.wrap(SPECIFICITY_EXCEPTION))
