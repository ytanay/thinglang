from thinglang.compiler.buffer import CompilationBuffer
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.common.list_type import ListInitialization
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.values.access import Access
from thinglang.parser.values.method_call import MethodCall


class InlineList(ListInitialization):
    """
    Describes inline list initialization
    """

    def __init__(self, values):
        super().__init__(values)
        self.inferred_type = None

    def replace_argument(self, idx, replacement):
        self.arguments[idx] = replacement

    def compile(self, context: CompilationBuffer):
        if not self.values:
            return

        buffer = context.optional()
        ref = self[0].compile(buffer)  # TODO: remove unnecessary recompilation of first element (used to infer type)

        list_type = GenericIdentifier(Identifier('list'), (ref.type,))
        last_call = MethodCall(Access([list_type, Identifier.constructor()])).deriving_from(self)

        for value in self:  # TODO: validate list is homogeneous, and descend to lowest common type
            last_call = MethodCall(Access([last_call, Identifier("append")]), ArgumentList([value])).deriving_from(self)

        return last_call.compile(context)

    def __repr__(self):
        return f'{self.arguments}'
