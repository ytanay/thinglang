from thinglang.lexer.blocks.conditionals import LexicalElse
from thinglang.parser.blocks.common import ElseBranchInterface
from thinglang.parser.blocks.conditional import Conditional
from thinglang.parser.rule import ParserRule


class ConditionalElse(Conditional, ElseBranchInterface):

    def __init__(self, conditional: Conditional):
        super(ConditionalElse, self).__init__(conditional.value)

    def describe(self):
        return 'else if {}'.format(self.value)

    @staticmethod
    @ParserRule.mark
    def parse_conditional_else(_: LexicalElse, conditional: Conditional):
        return ConditionalElse(conditional)
