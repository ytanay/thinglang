from thinglang import utils
from thinglang.execution.execution import ExecutionEngine
from thinglang.lexer.lexer import lexer
from thinglang.parser.analyzer import Analyzer
from thinglang.parser.parser import parse
from thinglang.parser.simplifier import Simplifier


def run(source):
    if not source:
        raise ValueError('Source cannot be empty')

    source = source.strip().replace(' ' * 4, '\t')

    utils.print_header('Source', source)

    lexical_groups = list(lexer(source))
    ast = parse(lexical_groups)

    Simplifier(ast).run()
    Analyzer(ast).run()

    utils.print_header('Parsed AST', ast.tree())

    with ExecutionEngine(ast) as engine:
        engine.execute()
        return engine.results()
