from thinglang.parser.nodes import BaseNode


class PassStatement(BaseNode):
    """
    Does nothing - generally used to fill out empty blocks
    """
    EMITTABLE = True
    MUST_CLOSE = False

    def __init__(self, raw, source_ref):
        super().__init__([])
        self.source_ref = source_ref

    def compile(self, context):  # TODO: assert no children
        return
