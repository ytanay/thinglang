import os

from thinglang import utils
from thinglang.compiler.indexer import Indexer, Collator
from thinglang.execution.execution import ExecutionEngine
from thinglang.lexer.lexer import lexer
from thinglang.parser.analyzer import Analyzer
from thinglang.parser.parser import parse
from thinglang.parser.simplifier import Simplifier

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'include')


def collect_includes():
    files = [os.path.join(BASE_DIR, path) for path in os.listdir(BASE_DIR)]
    return '\n' + '\n'.join(open(f).read() for f in files)


def compiler(source):
    if not source:
        raise ValueError('Source cannot be empty')

    source = source.strip().replace(' ' * 4, '\t')
    lexical_groups = list(lexer(source))
    ast = parse(lexical_groups)
    Simplifier(ast).run()
    Collator(ast).run()
    Indexer(ast).run()
    #Analyzer(ast).run()

    return ast

def run(source):
    ast = compiler(source)

    with ExecutionEngine(ast) as engine:
        engine.execute()
        return engine.results()
