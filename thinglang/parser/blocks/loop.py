from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeJumpConditional, OpcodeJump
from thinglang.parser.nodes.base_node import BaseNode


class Loop(BaseNode):

    def __init__(self, slice):
        super(Loop, self).__init__(slice)
        _, self.value = slice

    def describe(self):
        return str(self.value)

    def compile(self, context: CompilationContext):
        idx = context.current_index()
        self.value.compile(context)
        opcode = OpcodeJumpConditional()
        context.append(opcode, self.source_ref)
        super(Loop, self).compile(context)
        context.append(OpcodeJump(idx), self.source_ref)
        opcode.update(context.current_index())
