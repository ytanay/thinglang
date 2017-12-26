from thinglang.lexer.lexical_analyzer import lexer
from thinglang.parser import parser
from thinglang.parser.nodes.root_node import RootNode
from thinglang.utils import logging_utils
from thinglang.utils.source_context import SourceContext


def preprocess(source: SourceContext) -> RootNode:
    lexical_groups = lexer(source)
    ast = parser.parse(lexical_groups)
    ast.finalize()

    logging_utils.print_header("Original AST", ast.tree())

    return ast
