import os

import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENUM_PARSER = re.compile(r'(.*)\s*?=\s*?(\d+)')


def read_opcodes():
    with open(os.path.join(BASE_DIR, '..', 'serialization', 'Opcode.h')) as f:
        for line in f:
            if 'enum class Opcode' in line:
                break

        for decl in f:
            decl = decl.strip()

            if not decl:
                continue

            if '}' in decl:
                break

            groups = ENUM_PARSER.search(decl).groups()
            yield (groups[0].strip(), int(groups[1]))

OPCODES = dict(read_opcodes())

assert set(range(len(OPCODES))) == set(OPCODES.values())
