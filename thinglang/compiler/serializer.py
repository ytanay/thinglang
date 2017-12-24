import struct

from thinglang.lexer.values.identifier import Identifier


def auto(param):
    if isinstance(param, Identifier):
        return struct.pack('<I', len(param)) + bytes(param.value, 'utf-8')
