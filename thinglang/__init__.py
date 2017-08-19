from thinglang import utils
from thinglang.compiler import CompilationContext
from thinglang.compiler.indexer import Indexer
from thinglang.lexer.lexer import lexer
from thinglang.parser.nodes import RootNode
from thinglang.parser import parse
from thinglang.parser.simplifier import Simplifier
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.symbols.symbol_map import SymbolMap


def preprocess(source: str) -> RootNode:
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
    :param executable: should an executable file be made?
    :return: thinglang bytecode
    """

    ast = preprocess(source)

    symbols = SymbolMapper(ast)

    Simplifier(ast).run()
    Indexer(ast).run()

    utils.print_header("Final AST", ast.tree())

    context = CompilationContext(symbols, entry=symbols.entry() if executable else None)

    return ast.compile(context)
