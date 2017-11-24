import glob
import json
import os

from thinglang.symbols.symbol_map import SymbolMap
from thinglang.utils import collection_utils

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SYMBOL_PATTERN = os.path.join(CURRENT_PATH,  'symbols/**/*.thingsymbols')


@collection_utils.drain()
def read_foundation_symbols():
    """
    Reads and parses serialized thingsymbol files
    """
    for path in glob.glob(SYMBOL_PATTERN, recursive=True):
        with open(path, 'rb') as f:
            yield SymbolMap.from_serialized(json.load(f))
