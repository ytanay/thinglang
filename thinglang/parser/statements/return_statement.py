from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodeReturn
from thinglang.lexer.statements.return_statement import LexicalReturnStatement
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class ReturnStatement(BaseNode):
    """
    A return statement - can return a value or void
    """

    def __init__(self, value=None, token=None):
        super().__init__([value, token])
        self.value = value

    def __repr__(self):
        return f'return {self.value}'

    def compile(self, context: CompilationBuffer):
        if self.value is not None:
            self.value.compile(context)
        context.append(OpcodeReturn(), self.source_ref)

    @staticmethod
    @ParserRule.mark
    def parse_value_return(_: LexicalReturnStatement, value: ValueType):
        return ReturnStatement(value)

    @staticmethod
    @ParserRule.mark
    def parse_empty_return(_: LexicalReturnStatement):
        return ReturnStatement(token=_)
