from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeReturn
from thinglang.foundation import templates
from thinglang.parser.nodes import BaseNode


class ReturnStatement(BaseNode):
    def __init__(self, slice):
        super().__init__(slice)
        self.value = slice[1] if len(slice) == 2 else None

    def transpile(self):
        if not self.value:
            return templates.RETURN_NULL

        elif self.value.STATIC:
            return templates.RETURN_VALUE.format(value=self.value.transpile())
        else:
            return templates.RETURN_VALUE_INSTANTIATE.format(value=self.value.transpile())

    def compile(self, context: CompilationContext):
        self.value.compile(context)
        context.append(OpcodeReturn(), self.source_ref)
