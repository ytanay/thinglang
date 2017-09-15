from thinglang.parser.nodes.blocks.common import ElseBranchInterface
from thinglang.parser.nodes.blocks.conditional import Conditional


class ConditionalElse(Conditional, ElseBranchInterface):

    def __init__(self, slice):
        super(ConditionalElse, self).__init__(slice)
        _, self.conditional = slice

    def describe(self):
        return 'otherwise if {}'.format(self.value)
