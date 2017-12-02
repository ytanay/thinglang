from thinglang.lexer.operators.casts import LexicalCast
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.access import Access
from thinglang.parser.values.method_call import MethodCall
from thinglang.utils.type_descriptors import ValueType


class CastOperation(BaseNode):
    """
    Explicitly cast from one type to another
    Expects a conversion method on the source class
    """

    @staticmethod
    def create(source: Identifier, destination: Identifier) -> MethodCall:
        return MethodCall(Access([source, Identifier('convert_') + destination]), MethodCall.STACK_ARGS)

    @staticmethod
    @ParserRule.mark
    def parse_inline_cast_op(value: ValueType, _: LexicalCast, target_type: Identifier):
        return MethodCall(Access([value, Identifier('convert_') + target_type]), [])
