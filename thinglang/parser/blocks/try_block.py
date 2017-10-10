from thinglang.compiler.buffer import CompilationBuffer
from thinglang.lexer.blocks.exceptions import LexicalTry
from thinglang.parser.blocks.handle_block import HandleBlock
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule


class TryBlock(BaseNode):
    """
    Try blocks are used to generate exception handling tables during the final steps of the compilation process
    Essentially, the block tags all the instructions emitted by it, producing a range of instructions for which
    it is responsible for handling exceptions.

    """
    def __init__(self, token=None):
        super(TryBlock, self).__init__([token])

        self.handlers = None

    def finalize(self):
        super().finalize()
        self.handlers = self.siblings_while(lambda x: isinstance(x, HandleBlock))

        for handler in self.handlers:
            handler.remove()

    def compile(self, context: CompilationBuffer):
        start_index = context.next_index
        super(TryBlock, self).compile(context)
        end_index = context.current_index

        for handler in self.handlers:
            handler_idx = handler.compile(context)
            exception_type = context.symbols[handler.exception_type]
            context.add_entry(exception_type.index, handler_idx, start_index, end_index)

    @staticmethod
    @ParserRule.mark
    def parse_try_block(token: LexicalTry):
        return TryBlock(token)
