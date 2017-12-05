from thinglang import pipeline
from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.indexer import LocalMember
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.symbols.symbol_map import SymbolMap
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils.source_context import SourceContext

SELF_ID, A_ID, B_ID, INST_ID, LST_ID = 0, 1, 2, 3, 4
VAL1_ID, VAL2_ID, INNER_ID = 0, 1, 2
INNER1_ID, INNER2_ID = 0, 1


def compile_local(code):
    ast = pipeline.preprocess(SourceContext.wrap(code))
    symbols = SymbolMapper(override=[SymbolMap.from_serialized({
        "index": 0,
        "name": "Container",
        "extends": None,
        "offset": 0,
        "generics": [],
        "symbols": [
            {
                "arguments": None,
                "convention": "internal",
                "index": 0,
                "kind": "member",
                "name": "val1",
                "static": False,
                "type": "number"
            },
            {
                "arguments": None,
                "convention": "internal",
                "index": 1,
                "kind": "member",
                "name": "val2",
                "static": False,
                "type": "number"
            },
            {
                "arguments": None,
                "convention": "internal",
                "index": 2,
                "kind": "member",
                "name": "inner",
                "static": False,
                "type": "InnerContainer"
            },
            {
                "arguments": ["number"],
                "convention": "internal",
                "index": 3,
                "kind": "method",
                "name": "action",
                "static": False,
                "type": None
            }
        ]
    }), SymbolMap.from_serialized({
        "index": 1,
        "name": "InnerContainer",
        "extends": None,
        "offset": 0,
        "generics": [],
        "symbols": [
            {
                "arguments": None,
                "convention": "internal",
                "index": 0,
                "kind": "member",
                "name": "inner1",
                "static": False,
                "type": "number"
            },
            {
                "arguments": None,
                "convention": "internal",
                "index": 1,
                "kind": "member",
                "name": "inner2",
                "static": False,
                "type": "number"
            }
        ]
    })])

    buffer = CompilationBuffer(symbols, {
        Identifier.self(): LocalMember(Identifier('Container'), 0),
        Identifier('a'): LocalMember(Identifier('number'), A_ID),
        Identifier('b'): LocalMember(Identifier('number'), B_ID),
        Identifier('inst'): LocalMember(Identifier('Container'), INST_ID),
        Identifier('lst'): LocalMember(GenericIdentifier(Identifier('list'), (Identifier('number'),)), LST_ID)
    })

    return ast.compile(buffer).instructions
