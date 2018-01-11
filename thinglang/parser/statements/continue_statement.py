from thinglang.compiler.opcodes import OpcodeJump
from thinglang.parser.blocks.conditional import Conditional
from thinglang.parser.blocks.loop import Loop
from thinglang.parser.nodes import BaseNode


class ContinueStatement(BaseNode):
    """
    Jumps to the top of the currently executing loop
    """

    EMITTABLE = True
    MUST_CLOSE = False

    def __init__(self, raw, source_ref):
        super().__init__([])
        self.source_ref = source_ref

    def compile(self, context):  # TODO: assert no children
        container = self.ascend(Loop)
        if not container:
            raise Exception('Cannot break outside of loop') # TODO: should be StructureError
        context.append(OpcodeJump(context.jump_in[container]), self.source_ref)
