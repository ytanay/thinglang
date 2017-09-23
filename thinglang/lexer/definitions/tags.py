from thinglang.lexer.lexical_token import LexicalToken


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


class LexicalInheritanceTag(LexicalToken):
    """
    Tags a thing definition's parent type.
    """
