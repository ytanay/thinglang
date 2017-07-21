import os
import traceback

from thinglang import utils
from thinglang.compiler.indexer import Indexer, Collator
from thinglang.execution.execution import ExecutionEngine
from thinglang.lexer.lexer import lexer
from thinglang.parser.analyzer import Analyzer
from thinglang.parser.parser import parse
from thinglang.parser.simplifier import Simplifier
from thinglang.parser.symbols import RootNode

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'include')


def collect_includes():
    files = [os.path.join(BASE_DIR, path) for path in os.listdir(BASE_DIR)]
    return '\n' + '\n'.join(open(f).read() for f in files)


def preprocess(source) -> RootNode:
    if not source:
        raise ValueError('Source cannot be empty')

    source = source.strip().replace(' ' * 4, '\t')
    lexical_groups = lexer(source)
    ast = parse(lexical_groups)
    Simplifier(ast).run()
    return ast


def compiler(source: str, executable: bool=True):
    ast = preprocess(source)

    if executable:
        ast.reorder()

    Collator(ast).run()

    try:
        Indexer(ast).run()
    except Exception as e:
        print('Error during indexing: {}'.format(ast.tree()))
        traceback.print_exc()
        raise
    return ast


def run(source):
    ast = preprocess(source)

    with ExecutionEngine(ast) as engine:
        engine.execute()
        return engine.results()
