from thinglang.compiler.context import CompilationContext
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.common.list_type import ListInitialization
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.values.access import Access
from thinglang.parser.values.method_call import MethodCall


class InlineList(ListInitialization):

    def replace_argument(self, idx, replacement):
        self.arguments[idx] = replacement

    def compile(self, context: CompilationContext):
        last_call = MethodCall(Access([Identifier("list"), Identifier.constructor()])).deriving_from(self)

        for value in self:
            last_call = MethodCall(Access([last_call, Identifier("append")]), ArgumentList([value])).deriving_from(self)

        return last_call.compile(context)
