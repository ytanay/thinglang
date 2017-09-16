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


class LexicalDeclarationConstructor(LexicalToken):
    """
    Declares a constructor.

    Examples:
        setup
        setup with number size
    """


class LexicalDeclarationStatic(LexicalToken):
    """
    Tags a definition as static.

    Examples:
        does static hello_message
        has static text count
    """


class LexicalDeclarationReturnType(LexicalToken):
    """
    Tags a method's return type.

    Examples:
        does get_text returns text
    """


class LexicalArgumentListIndicator(LexicalToken):
    """
    Tags a method's arguments.

    Examples:
        does add with number lhs, number rhs
    """


