from thinglang.compiler.context import CompilationContext
from thinglang.phases.preprocess import preprocess
from thinglang.phases.indexer import Indexer
from thinglang.phases.integrity import StructuralIntegrity
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils import logging_utils
from thinglang.utils.source_context import SourceContext


def compile(entrypoint: SourceContext, executable: bool=True, mapper: SymbolMapper=None) -> CompilationContext:
    """
    Compile a thinglang program
    :param entrypoint: file path of the program entrypoint
    :param executable: should an executable file be made?
    :param mapper: optionally, an existing SymbolMapper to use
    :return: thinglang bytecode
    """

    ast = preprocess(entrypoint)
    mapper = SymbolMapper(ast) if mapper is None else mapper.set_ast(ast)

    StructuralIntegrity(ast).run()
    Indexer(ast).run()
    logging_utils.print_header("Final AST", ast.tree())

    context = CompilationContext(mapper, entrypoint, entry=mapper.entry() if executable else None)

    return ast.compile(context)
