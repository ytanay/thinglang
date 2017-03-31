from thinglang.parser.tokens.collections import ListInitializationPartial, ListInitialization
from thinglang.utils.type_descriptors import ValueType


class ArrayInitializationPartial(ListInitializationPartial):
    pass


class ArrayInitialization(ListInitialization, ValueType):
    pass
