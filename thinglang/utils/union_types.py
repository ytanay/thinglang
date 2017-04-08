from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.parser.symbols.functions import Access, MethodCall
from thinglang.parser.symbols.types import ArrayInitialization, CastOperation
from thinglang.utils.type_descriptors import ValueType

ACCESS_TYPES = Access, LexicalIdentifier
POTENTIALLY_RESOLVABLE = Access, LexicalIdentifier, ValueType
POTENTIALLY_OBTAINABLE = MethodCall, ArithmeticOperation, ArrayInitialization, CastOperation
