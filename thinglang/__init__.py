from thinglang import utils
from thinglang.compiler import CompilationContext
from thinglang.compiler.indexer import Indexer, Collator
from thinglang.lexer.lexer import lexer
from thinglang.parser.nodes import RootNode
from thinglang.parser.parser import parse
from thinglang.parser.simplifier import Simplifier
from thinglang.parser.symbols import SymbolMap


def parser(source: str) -> RootNode:
    if not source:
        raise ValueError('Source cannot be empty')

    source = source.strip().replace(' ' * 4, '\t')
    lexical_groups = lexer(source)
    ast = parse(lexical_groups)

    utils.print_header("Original AST", ast.tree())

    return ast


def compile(source: str, executable: bool=True) -> CompilationContext:
    """
    Compile a thinglang program
    :param source: source code of main module
    :param executable: should an executable be generated?
    :return: thinglang bytecode
    """

    ast = parser(source)

    if executable:
        ast.reorder()

    Simplifier(ast).run()
    Collator(ast).run()
    Indexer(ast).run()

    symbols = SymbolMap(ast.children[0])

    utils.print_header('Symbols', symbols, pretty=True)

    return ast.compile()
