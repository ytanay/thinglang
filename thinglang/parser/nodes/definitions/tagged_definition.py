from thinglang.parser.nodes import BaseNode
from thinglang.utils.type_descriptors import ValueType


class TaggedDeclaration(BaseNode, ValueType):

    @classmethod
    def construct(cls, slice):
        slice[1].static_member = True
        return slice[1]
