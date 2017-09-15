from thinglang.lexer import LexicalToken


class InlineCode(LexicalToken):
    STATIC = True

    def __init__(self, value, source_ref):
        super(InlineCode, self).__init__(value, source_ref)
        self.children = []

    def tree(self, depth):
        return self.value
