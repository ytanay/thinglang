from thinglang.phases.preprocess import preprocess
from thinglang.compiler.context import CompilationContext
from thinglang.compiler.indexer import Indexer
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils import logging_utils
from thinglang.utils.source_context import SourceContext


def compile(entrypoint: SourceContext, executable: bool=True, mapper: SymbolMapper=None) -> CompilationContext:
    """
    Compile a thinglang program
    :param entrypoint: file path of the program entrypoint
    :param executable: should an executable file be made?
    :return: thinglang bytecode
    """

    ast = preprocess(entrypoint)

    symbols = SymbolMapper(ast)

    Indexer(ast).run()

    logging_utils.print_header("Final AST", ast.tree())

    context = CompilationContext(symbols, entrypoint, entry=symbols.entry() if executable else None)

    return ast.compile(context)
