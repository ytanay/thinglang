from thinglang.lexer.tokens import LexicalToken


class LexicalReturnStatement(LexicalToken):
    pass


class LexicalArgumentListIndicator(LexicalToken):
    pass


class LexicalDeclarationMethod(LexicalToken):
    def __init__(self, value, source_ref):
        super().__init__(value, source_ref)
        self.static_member = False


class LexicalDeclarationStatic(LexicalToken):
    pass


class LexicalDeclarationConstructor(LexicalToken):
    pass


class LexicalDeclarationReturnType(LexicalToken):
    pass


class LexicalClassInitialization(LexicalToken):
    pass


class LexicalDeclarationThing(LexicalToken):
    pass


class LexicalDeclarationMember(LexicalToken):
    pass
