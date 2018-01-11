import collections

from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.errors import DuplicateHandlerError, ExceptionSpecificityError, NoExceptionHandlers
from thinglang.lexer.blocks.exceptions import LexicalTry
from thinglang.parser.blocks.handle_block import HandleBlock
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule

ExceptionEntry = collections.namedtuple('ExceptionEntry', ['exception_type', 'handler', 'range_start', 'range_end'])


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

        if len({handler.exception_type for handler in self.handlers}) != len(self.handlers):
            raise DuplicateHandlerError([handler.exception_type for handler in self.handlers])

        if not self.handlers:
            raise NoExceptionHandlers(self)

        for handler in self.handlers:
            handler.remove()

    def compile(self, context: CompilationBuffer):
        start_index = context.next_index
        super(TryBlock, self).compile(context)
        end_index = context.current_index

        # We always execute the first handler which can accepts the given exception

        entries = []

        for handler in self.handlers:
            handler_idx = handler.compile(context)
            specified_exception = context.symbols[handler.exception_type]

            # Verify this entry is less specific than all previously compiled entries
            for entry in entries:
                if specified_exception in context.symbols.descendants(entry.exception_type):
                    raise ExceptionSpecificityError(specified_exception, entry.exception_type)

            for exception_type in context.symbols.descendants(specified_exception):
                if exception_type not in [entry.exception_type for entry in entries]:  # Is this check redundant?
                    entries.append(ExceptionEntry(exception_type, handler_idx, start_index, end_index))

        context.add_entries(entries)

    @staticmethod
    @ParserRule.mark
    def parse_try_block(token: LexicalTry):
        return TryBlock(token)
