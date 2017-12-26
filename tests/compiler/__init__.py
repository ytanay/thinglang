import itertools

from thinglang import pipeline
from thinglang.compiler.opcodes import OpcodeCallInternal
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.cast_tag import CastTag
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils.source_context import SourceContext

SELF_ID, A_ID, B_ID, INST_ID, LST_ID, A_INST, B_INST, C_INST, IMPLICIT_ITERATOR_ID, IMPLICIT_ITERATION_ID = range(10)
VAL1_ID, VAL2_ID, INNER_ID = 0, 1, 2
INNER1_ID, INNER2_ID = 0, 1
STATIC_START = 6

PROGRAM, CONTAINER, A_THING, B_THING, C_THING = range(5)

SYMBOL_MAPPER = SymbolMapper()

TEMPLATE = """
thing Program
    has number val1
    has number val2
    has Container inner
    
    setup
        number a = 0
        number b = 0
        Program inst = Program()
        list<number> lst = [0, 1, 2]
        A a_inst = A()
        B b_inst = B(42)
        C c_inst = C()
        
        {}
    
    does action with number n 
        Console.print("action")
        
    does add with number a, number b
        return a + b


thing Container
    has number inner1
    has number inner2
    
thing A
    has number a1

thing B extends A
    has number b1
    
    setup with number b1
        self.b1 = b1
        
thing C extends B
    has number c1
    
    
        
"""


def compile_base(code='', thing_id=0, method_id=0, trim=False):
    context = pipeline.compile(SourceContext.wrap(code), mapper=SYMBOL_MAPPER)
    entry = context.methods[(thing_id, method_id)]
    instructions = entry[1].instructions
    return instructions[trim + 1:-1] if trim else instructions


def compile_template(code='', thing_id=0, method_id=0):
    return compile_base(TEMPLATE.format(code), thing_id, method_id)


TRIM_START = len(compile_template()) - 1


def compile_snippet(code):
    instructions = compile_template(code)[TRIM_START:-1]  # Pop off boilerplate and the return instruction
    print('Bytecode result: {}'.format(instructions))
    return instructions


def internal_call(target):
    return OpcodeCallInternal.from_reference(SYMBOL_MAPPER.resolve_named([
        CastTag.parse(x) if CastTag.matches(x) else Identifier(x) for x in target.split('.')
    ]))
