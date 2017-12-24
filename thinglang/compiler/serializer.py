import struct

from thinglang.lexer.values.identifier import Identifier


def auto(param):
    if isinstance(param, Identifier):
        return pack_str(param.value)

    if isinstance(param, str):
        return pack_str(param)

    raise Exception('Cannot serialize {}'.format(param))


def pack_str(param):
    return struct.pack('<I', len(param)) + bytes(param, 'utf-8')
