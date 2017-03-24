import abc

from thinglang.lexer.symbols import LexicalSymbol


class LexicalComparison(LexicalSymbol, metaclass=abc.ABCMeta):  # one of eq, neq, >, <, etc...
    pass


class LexicalConditional(LexicalSymbol):  # if conditional
    pass


class LexicalElse(LexicalSymbol):  # otherwise
    pass


class LexicalEquality(LexicalComparison):  # lhs eq rhs
    pass
