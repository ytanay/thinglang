from thinglang.lexer.lexical_token import LexicalToken


class LexicalDeclarationThing(LexicalToken):
    """
    Begins a thing definition.

    Examples:
        thing Program
    """


class LexicalDeclarationMethod(LexicalToken):
    """
    Declares a method.

    Examples:
        does say_hello
        does walk with Location target
        does format returns text
    """
    def __init__(self, value, source_ref):
        super().__init__(value, source_ref)
        self.static_member = False


class LexicalDeclarationMember(LexicalToken):
    """
    Declares a member.

    Examples:
        has text name
        has number age
    """

