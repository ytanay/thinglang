from thinglang.lexer.values.numeric import NumericValue


class LexicalBoolean(NumericValue):
    """
    The base boolean type.
    """


class LexicalBooleanTrue(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanTrue, self).__init__(True, source_ref)

    def transpile(self):
        return 'BOOL_TRUE'


class LexicalBooleanFalse(LexicalBoolean):

    def __init__(self, _, source_ref):
        super(LexicalBooleanFalse, self).__init__(False, source_ref)

    def transpile(self):
        return 'BOOL_FALSE'
