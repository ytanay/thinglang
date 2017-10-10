from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodePass, OpcodeJump
from thinglang.lexer.blocks.exceptions import LexicalHandle
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule


class HandleBlock(BaseNode):

    def __init__(self, exception_type, exception_name):
        super(HandleBlock, self).__init__([exception_type, exception_name])
        self.exception_type, self.exception_name = exception_type, exception_name

    def compile(self, context: CompilationBuffer):
        assert self.parent is None, 'Handle blocks may not be part of the AST after finalization'

        buffer = context.optional()
        super(HandleBlock, self).compile(buffer)
        buffer.append(OpcodeJump(context.next_index, absolute=True), self.source_ref)
        return context.epilogue(buffer)

    @staticmethod
    @ParserRule.mark
    def parse_handle_block(_: LexicalHandle, exception_type: Identifier, exception_name: Identifier):
        return HandleBlock(exception_type, exception_name)
