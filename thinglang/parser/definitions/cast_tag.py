from thinglang.lexer.values.identifier import Identifier


class CastTag(object):

    PREFIX = 'as '

    def __init__(self, destination_type):
        self.destination_type = destination_type

    def __hash__(self):
        return hash(self.destination_type)

    def __eq__(self, other):
        return type(self) == type(other) and self.destination_type == other.destination_type

    def __repr__(self):
        return f'as {self.destination_type}'

    def deriving_from(self, *args, **kwargs):
        pass

    @classmethod
    def parse(cls, param):
        return cls(Identifier(param[len(CastTag.PREFIX):]))

    @classmethod
    def matches(cls, param):
        return param.startswith(CastTag.PREFIX)