from thinglang.lexer.lexical_token import LexicalToken


class LexicalGroupEnd(LexicalToken):
    """
    Emitted at the end of every source line.

    Used to define parsing rules that explicitly terminate a source group, and to aid the vectorization process
    """
    def __init__(self):
        super(LexicalGroupEnd, self).__init__(None, None)