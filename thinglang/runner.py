from thinglang.execution.execution import ExecutionEngine
from thinglang.lexer.lexer import lexer
from thinglang.parser.parser import parse
from thinglang.parser.simplifier import simplify


def run(source):
    if not source:
        raise ValueError('Source cannot be empty')

    source = source.strip().replace(' ' * 4, '\t')

    lexical_groups = list(lexer(source))
    tree = parse(lexical_groups)
    root_node = simplify(tree)

    with ExecutionEngine(root_node) as engine:
        engine.execute()
        return engine.results()
