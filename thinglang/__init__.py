import os

from thinglang import utils
from thinglang.execution.execution import ExecutionEngine
from thinglang.lexer.lexer import lexer
from thinglang.parser.analyzer import Analyzer
from thinglang.parser.parser import parse
from thinglang.parser.simplifier import Simplifier

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'include')


def collect_includes():
    files = [os.path.join(BASE_DIR, path) for path in os.listdir(BASE_DIR)]
    return '\n' + '\n'.join(open(f).read() for f in files)


def run(source):
    if not source:
        raise ValueError('Source cannot be empty')

    source = (source + collect_includes()).strip().replace(' ' * 4, '\t')

    utils.print_header('Source', source)

    lexical_groups = list(lexer(source))
    ast = parse(lexical_groups)

    Simplifier(ast).run()

    utils.print_header('C++ Transpilation', ast.transpile_children())
    utils.print_header('Parsed AST', ast.tree())

    Analyzer(ast).run()

    with ExecutionEngine(ast) as engine:
        engine.execute()
        return engine.results()
