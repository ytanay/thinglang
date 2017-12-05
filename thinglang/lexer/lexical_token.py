from thinglang.utils.logging_utils import camelcase_to_underscore


class LexicalToken(object):
    """
    The base lexical token object
    """

    EMITTABLE = True  # Should this token be emitted into the token stream?
    STATIC = False  # Does this token refer to statically known data (e.g. an inline string/numeric value)
    ALLOW_EMPTY = False  # Can this token be generated with a zero-sized buffer?
    MUST_CLOSE = False  # Does this token have a closing counterpart (e.g. parentheses)

    def __init__(self, value, source_ref):
        self.value, self.source_ref = value, source_ref

    @classmethod
    def next_operator_set(cls, current, original):
        """
        Optionally, returns the set of allowed operators after this token
        """
        return current

    def transpile(self):
        return self.value

    def __eq__(self, other):
        return type(self) is type(other) and \
               self.value == other.value

    def __hash__(self):
        return hash((type(self), self.value))

    def __repr__(self):
        return type(self).__name__

    @classmethod
    def format_name(cls):
        return '__{}__'.format(camelcase_to_underscore(cls.__name__.replace('Lexical', '')))
