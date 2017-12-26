from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.phases import preprocess
from thinglang.utils.source_context import SourceContext


class InlineCandidate(object):

    def __init__(self, nodes, arguments):
        assert len(nodes) <= 1, len(nodes)
        self.nodes, self.arguments = nodes, arguments

    def serialize(self):
        return {
            "code": self.nodes[0].source_ref.source_line.source.strip(),
            "argument_names": [repr(x) for x in self.arguments]
        } if self.nodes else None

    @classmethod
    def from_method(cls, method):
        if method.static and method.return_type is None:  # TODO: assert explicit locals == 0
            return cls(method.children, method.arguments)

    @classmethod
    def from_serialized(cls, code, argument_names, argument_types):
        ast = preprocess.preprocess(SourceContext.wrap(code))
        return cls(ast.children, ArgumentList([
            Identifier(name, type_name=arg_type) for name, arg_type in zip(argument_names, argument_types)
        ]))
