from thinglang import pipeline
from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.indexer import LocalMember
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.symbols.symbol_map import SymbolMap
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils.source_context import SourceContext

SELF_ID, A_ID, B_ID, INST_ID, LST_ID, IMPLICIT_ITERATOR_ID, IMPLICIT_ITERATION_ID = 0, 1, 2, 3, 4, 5, 6
VAL1_ID, VAL2_ID, INNER_ID = 0, 1, 2
INNER1_ID, INNER2_ID = 0, 1
STATIC_START = 5


TEMPLATE = """
thing Program
    has number val1
    has number val2
    has Container inner
    
    setup
        number a = 0
        number b = 0
        Program inst = create Program()
        list<number> lst = [0, 1, 2]
        
        {}
    
    does action with number n 
        Console.print("action")


thing Container
    has number inner1
    has number inner2    
"""


def compile_base(code):
    context = pipeline.compile(SourceContext.wrap(TEMPLATE.format(code)))
    entry = context.methods[(0, 0)]
    return entry[1].instructions


TRIM_START = len(compile_base('')) - 1


def compile_local(code):
    return compile_base(code)[TRIM_START:-1]  # Pop off boilerplate and the return instruction

