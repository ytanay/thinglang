from thinglang.lexer.values.identifier import Identifier


class CastTag(Identifier):

    def __init__(self, destination_type):
        super().__init__(f'as {destination_type}', validate=False)
        self.destination_type = destination_type

    def __hash__(self):
        return hash(self.destination_type)

    def __eq__(self, other):
        return type(self) == type(other) and self.destination_type == other.destination_type

    def __repr__(self):
        return f'as {self.destination_type}'

    def deriving_from(self, *args, **kwargs):
        pass

    def serialize(self):
        return {
            "intent": "cast",
            "type": self.destination_type
        }
