from thinglang.compiler.references import Reference
from thinglang.lexer.operators.casts import LexicalCast
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.named_access import NamedAccess
from thinglang.parser.values.method_call import MethodCall
from thinglang.utils.type_descriptors import ValueType


class CastOperation(BaseNode):
    """
    Explicitly cast from one type to another
    Expects a conversion method on the source class
    """

    @staticmethod
    def create(source: Reference, destination_type: Identifier) -> MethodCall:
        return MethodCall(NamedAccess([source.type, Identifier('convert_') + destination_type]), [source], stack_args=True)

    @staticmethod
    @ParserRule.mark
    def parse_inline_cast_op(value: ValueType, _: LexicalCast, target_type: Identifier):
        return MethodCall(NamedAccess.extend(value, Identifier('convert_') + target_type), [])
