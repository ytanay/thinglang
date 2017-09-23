from thinglang.parser.nodes.base_node import BaseNode
from thinglang.utils.type_descriptors import ValueType


class TaggedMethodDeclaration(BaseNode, ValueType):

    @classmethod
    def construct(cls, slice):
        slice[1].static_member = True
        return slice[1]


class TaggedThingDefinition(BaseNode):

    @classmethod
    def construct(cls, slice):
        slice[0].extends = slice[2]
        return slice[0]
