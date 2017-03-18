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
    validate(tree)
    root_node = simplify(tree)
    validate(tree)

    with ExecutionEngine(root_node) as engine:
        engine.execute()
        return engine.results()


def validate(node, parent=None):
    assert node.parent is parent, 'expected node {} to have parent {} but got {}'.format(node, parent, node.parent)
    for child in node.children:
        validate(child, node)