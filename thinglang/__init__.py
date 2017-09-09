from thinglang.utils import logging_utils
from thinglang.compiler import CompilationContext
from thinglang.compiler.indexer import Indexer
from thinglang.lexer import lexer
from thinglang.parser.nodes import RootNode
from thinglang.parser import parse
from thinglang.parser.simplifier import Simplifier
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.symbols.symbol_map import SymbolMap
from thinglang.utils.source_context import SourceContext


def preprocess(source: SourceContext) -> RootNode:
    lexical_groups = lexer(source)
    ast = parse(lexical_groups)

    logging_utils.print_header("Original AST", ast.tree())

    return ast


def compile(entrypoint: SourceContext, executable: bool=True) -> CompilationContext:
    """
    Compile a thinglang program
    :param entrypoint: file path of the program entrypoint
    :param executable: should an executable file be made?
    :return: thinglang bytecode
    """

    ast = preprocess(entrypoint)

    symbols = SymbolMapper(ast)

    Simplifier(ast).run()
    Indexer(ast).run()

    logging_utils.print_header("Final AST", ast.tree())

    context = CompilationContext(symbols, entrypoint, entry=symbols.entry() if executable else None)

    return ast.compile(context)
