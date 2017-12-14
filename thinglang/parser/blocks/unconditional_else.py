from thinglang.compiler.buffer import CompilationBuffer
from thinglang.foundation import templates
from thinglang.lexer.blocks.conditionals import LexicalElse
from thinglang.parser.blocks.common import ElseBranchInterface
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule


class UnconditionalElse(BaseNode, ElseBranchInterface):
    """
    An unconditional else block
    Must be preceded by a Conditional
    """

    def __init__(self, token):
        super(UnconditionalElse, self).__init__(token)

    def __repr__(self):
        return 'else'

    def compile(self, context: CompilationBuffer):
        super(UnconditionalElse, self).compile(context)
        context.update_conditional_jumps()

    @staticmethod
    @ParserRule.mark
    def parse_unconditional_else(_: LexicalElse):
        return UnconditionalElse([_])
