from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeJump, OpcodePass
from thinglang.lexer.blocks.exceptions import LexicalTry, LexicalHandle
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule


class TryBlock(BaseNode):

    def __init__(self, token=None):
        super(TryBlock, self).__init__([token])

    @staticmethod
    @ParserRule.mark
    def parse_try_block(token: LexicalTry):
        return TryBlock(token)


class HandleBlock(BaseNode):

    def __init__(self, exception_type, exception_name):
        super(HandleBlock, self).__init__([exception_type, exception_name])
        self.exception_type, self.exception_name = exception_type, exception_name

    def compile(self, context: CompilationContext):
        buffer = context.buffer()
        buffer.append(OpcodePass(), self.source_ref)
        super(HandleBlock, self).compile(buffer)
        buffer.append(OpcodeJump(context.current_index() + 1), self.source_ref)
        context.epilogue(buffer)

    @staticmethod
    @ParserRule.mark
    def parse_handle_block(_: LexicalHandle, exception_type: Identifier, exception_name: Identifier):
        return HandleBlock(exception_type, exception_name)
