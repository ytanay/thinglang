from thinglang.compiler.references import Reference
from thinglang.lexer.operators.casts import LexicalCast
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.cast_tag import CastTag
from thinglang.parser.nodes import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.values.method_call import MethodCall
from thinglang.parser.values.named_access import NamedAccess
from thinglang.utils.type_descriptors import ValueType, CallSite


class CastOperation(BaseNode, ValueType, CallSite):
    """
    Explicitly cast from one type to another
    Expects a conversion method on the source class
    """

    def __init__(self, value, target_type: Identifier, stack_args=False, stack_target=False):
        super().__init__([value])
        self.value, self.target_type, self.stack_args, self.stack_target = value, target_type, stack_args, stack_target

    def compile(self, context):
        if self.redundant(context):
            return self.value.compile(context)

        return MethodCall(NamedAccess.extend(self.value, CastTag(self.target_type)), stack_args=self.stack_args, stack_target=self.stack_target).compile(context)

    def replace_references(self, replacements):
        return CastOperation(replacements[self.value], self.target_type, stack_args=self.stack_args)

    @staticmethod
    @ParserRule.mark
    def parse_inline_cast_op(value: ValueType, _: LexicalCast, target_type: Identifier):
        return CastOperation(value, target_type)

    def redundant(self, context):  #TODO test this
        actual_value = self.value if isinstance(self.value, Reference) else self.value.compile(context.optional())
        return any(parent_type.name == self.target_type for parent_type in context.symbols.inheritance(actual_value.type)) # TODO: lifted from ArgumentSelector
