from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.nodes.functions import Access
from thinglang.utils.type_descriptors import ValueType

ACCESS_TYPES = Access, LexicalIdentifier
POTENTIALLY_RESOLVABLE = Access, LexicalIdentifier, ValueType
