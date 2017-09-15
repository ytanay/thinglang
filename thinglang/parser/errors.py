class ParserError(Exception):
    pass


class VectorReductionError(ParserError):
    """
    A generic parser error, thrown when a vector of lexical tokens could not be
    entirely reduced - that is to say, invalid syntax was supplied by the user.
    """
