from thinglang.parser.tokens.base import ListInitializationPartial, ListInitialization
from thinglang.utils.type_descriptors import ValueType


class ArrayInitializationPartial(ListInitializationPartial):
    pass


class ArrayInitialization(ListInitialization, ValueType):
    pass
