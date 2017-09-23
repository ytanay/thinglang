from thinglang.parser.blocks.common import ElseBranchInterface
from thinglang.parser.blocks.conditional import Conditional


class ConditionalElse(Conditional, ElseBranchInterface):

    def __init__(self, slice):
        super(ConditionalElse, self).__init__(slice)
        _, self.conditional = slice

    def describe(self):
        return 'else if {}'.format(self.value)
