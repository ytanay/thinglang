from thinglang.parser.nodes import BaseNode


class DefinitionPairNode(BaseNode):
    def __init__(self, slice):
        super(DefinitionPairNode, self).__init__(slice)
        self.name = slice[1]