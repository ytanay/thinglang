from thinglang import compiler
from thinglang.proto.bytecode_pb2 import Bytecode


def serialize(ast, bytecode):
    symbol = ast.serialize()
    bytecode.symbol.extend([symbol])
    for x in ast.children:
        serialize(x, bytecode)

    return bytecode

ast = compiler("""
thing Program
    setup
        number i = 5
        Output.write("hello world", i)
""")

bc = serialize(ast, Bytecode())
#print(bc)
