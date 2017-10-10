from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeReturn
from thinglang.foundation import templates
from thinglang.lexer.statements.return_statement import LexicalReturnStatement
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.utils.type_descriptors import ValueType


class ReturnStatement(BaseNode):
    def __init__(self, value=None, token=None):
        super().__init__([value, token])
        self.value = value

    def transpile(self):
        if not self.value:
            return templates.RETURN_NULL

        elif self.value.STATIC:
            return templates.RETURN_VALUE.format(value=self.value.transpile())
        else:
            return templates.RETURN_VALUE_INSTANTIATE.format(
                value=self.value.transpile(),
                instance_cls_name=self.container_name[1]
            )

    def compile(self, context: CompilationBuffer):
        if self.value is not None:
            self.value.compile(context)
        context.append(OpcodeReturn(), self.source_ref)

    @staticmethod
    @ParserRule.mark
    def parse_value_return(_: LexicalReturnStatement, value: ValueType):
        return ReturnStatement(value)

    @staticmethod
    @ParserRule.mark
    def parse_empty_return(_: LexicalReturnStatement):
        return ReturnStatement(token=_)
