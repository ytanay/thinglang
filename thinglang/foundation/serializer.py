import glob
import json
import os

from thinglang.symbols.symbol_map import SymbolMap

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SYMBOL_PATTERN = os.path.join(CURRENT_PATH,  'symbols/**/*.thingsymbols')


def read_foundation_symbols():
    return [read_symbols(path) for path in glob.glob(SYMBOL_PATTERN, recursive=True)]


def read_symbols(path):
    with open(path, 'rb') as f:
        symbols = json.load(f)

    return SymbolMap.from_serialized(symbols)


