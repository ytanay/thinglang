from thinglang.compiler.context import CompilationContext
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.common.list_type import ListInitialization
from thinglang.parser.values.method_call import MethodCall


class InlineList(ListInitialization):
    def compile(self, context: CompilationContext):
        last_call = MethodCall.create([Identifier("list"), Identifier.constructor()]).deriving_from(self)

        for value in self:
            last_call = MethodCall.create([last_call, Identifier("append")], [value]).deriving_from(self)

        last_call.compile(context)
