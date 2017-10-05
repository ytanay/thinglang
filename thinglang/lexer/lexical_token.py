from thinglang.utils.logging_utils import camelcase_to_underscore


class LexicalToken(object):
    EMITTABLE = True
    STATIC = False
    ALLOW_EMPTY = False
    MUST_CLOSE = False

    def __init__(self, value, source_ref):
        self.value, self.source_ref = value, source_ref

    @classmethod
    def next_operator_set(cls, current, original):
        return current

    def transpile(self):
        return self.value

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.value == other.value

    def __hash__(self):
        return hash((type(self), self.value))

    @classmethod
    def format_name(cls):
        return '__{}__'.format(camelcase_to_underscore(cls.__name__.replace('Lexical', '')))