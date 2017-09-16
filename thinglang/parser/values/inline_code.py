from thinglang.lexer.tokens import LexicalToken
from thinglang.utils.type_descriptors import ValueType


class InlineCode(LexicalToken, ValueType):
    STATIC = True

    def __init__(self, value, source_ref):
        super(InlineCode, self).__init__(value, source_ref)
        self.children = []

    def tree(self, depth):
        return self.value

    def finalize(self):
        pass
