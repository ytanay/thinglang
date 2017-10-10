from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodeThrow
from thinglang.lexer.statements.throw_statement import LexicalThrowStatement
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class ThrowStatement(BaseNode):
    def __init__(self, value=None):
        super().__init__([value])
        self.value = value

    def compile(self, context: CompilationBuffer):
        self.value.compile(context)
        context.append(OpcodeThrow(), self.source_ref)

    @staticmethod
    @ParserRule.mark
    def parse_throw_statement(_: LexicalThrowStatement, value: ValueType):
        return ThrowStatement(value)
