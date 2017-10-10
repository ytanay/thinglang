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

    def compile(self, context: CompilationBuffer):
        assert self.parent is None
        optional = context.optional()
        optional.append(OpcodePass(), self.source_ref)
        super(HandleBlock, self).compile(optional)
        optional.append(OpcodeJump(context.next_index), self.source_ref)
        return context.epilogue(optional)

    @staticmethod
    @ParserRule.mark
    def parse_handle_block(_: LexicalHandle, exception_type: Identifier, exception_name: Identifier):
        return HandleBlock(exception_type, exception_name)
