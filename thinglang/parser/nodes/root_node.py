from thinglang.parser.nodes import BaseNode


class RootNode(BaseNode):
    def __init__(self):
        super(RootNode, self).__init__(())

    def compile(self, context):
        super(RootNode, self).compile(context)
        return context

    def transpile(self):
        return self.transpile_children()
