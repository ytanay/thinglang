from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.arithmetic import ArithmeticOperation
from thinglang.parser.nodes.functions import Access, MethodCall
from thinglang.parser.nodes.types import ArrayInitialization, CastOperation
from thinglang.utils.type_descriptors import ValueType

ACCESS_TYPES = Access, LexicalIdentifier
POTENTIALLY_RESOLVABLE = Access, LexicalIdentifier, ValueType
POTENTIALLY_OBTAINABLE = MethodCall, ArithmeticOperation, ArrayInitialization, CastOperation
