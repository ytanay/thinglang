from thinglang import pipeline
from thinglang.compiler.context import CompilationContext
from thinglang.symbols.symbol_mapper import SymbolMapper, SymbolMap
from thinglang.utils.source_context import SourceContext
from thinglang.compiler.indexer import LocalMember
from thinglang.compiler.opcodes import OpcodeAssignStatic, OpcodeAssignLocal, OpcodePushMember, OpcodePopLocal, \
    OpcodeDereference
from thinglang.lexer.values.identifier import Identifier


def compile_local(code):
    ast = pipeline.preprocess(SourceContext.wrap(code))
    symbols = SymbolMapper(override=[SymbolMap.from_serialized({
        "index": 0,
        "name": "Container",
        "extends": None,
        "offset": 0,
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
            }
        ]
    }), SymbolMap.from_serialized({
        "index": 1,
        "name": "InnerContainer",
        "extends": None,
        "offset": 0,
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
    context = CompilationContext(symbols, SourceContext.wrap(''))
    context.current_locals = {
        Identifier.self(): LocalMember(Identifier('Container'), 0),
        Identifier('a'): LocalMember(Identifier('number'), 1),
        Identifier('b'): LocalMember(Identifier('number'), 2),
        Identifier('inst'): LocalMember(Identifier('Container'), 3),
    }
    return ast.compile(context).instruction_block


def test_static_to_local():
    assert compile_local('a = 5') == [OpcodeAssignStatic(1, 0)]
    assert compile_local('a = "hello"') == [OpcodeAssignStatic(1, 0)]


def test_local_to_local():
    assert compile_local('a = b') == [OpcodeAssignLocal(1, 2)]


def test_self_member_to_local():
    assert compile_local('a = self.val1') == [OpcodePushMember(0, 0), OpcodePopLocal(1)]
    assert compile_local('b = self.val2') == [OpcodePushMember(0, 1), OpcodePopLocal(2)]


def test_member_to_local():
    assert compile_local('a = inst.val1') == [OpcodePushMember(3, 0), OpcodePopLocal(1)]
    assert compile_local('b = inst.val2') == [OpcodePushMember(3, 1), OpcodePopLocal(2)]


def test_inner_self_member_to_local():
    assert compile_local('a = self.inner.inner1') == [OpcodePushMember(0, 2), OpcodeDereference(0), OpcodePopLocal(1)]
    assert compile_local('b = self.inner.inner2') == [OpcodePushMember(0, 2), OpcodeDereference(1), OpcodePopLocal(2)]


def test_inner_member_to_local():
    assert compile_local('a = inst.inner.inner1') == [OpcodePushMember(3, 2), OpcodeDereference(0), OpcodePopLocal(1)]
    assert compile_local('b = inst.inner.inner2') == [OpcodePushMember(3, 2), OpcodeDereference(1), OpcodePopLocal(2)]


