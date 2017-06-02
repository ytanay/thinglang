import os

import json
import random
import string

INDENT = '\n' + ' ' * 8


def generate_simple_output_program(source):
    return """thing Program
    setup{source}
    """.format(source=INDENT + INDENT.join([source] if isinstance(source, str) else source))


def generate_test_case_structure(dct):
    lst = []
    for name, groups in list(dct.items()):
        for idx, group in enumerate(groups):
            lst.append(('{} #{}'.format(name, idx + 1), group[0], group[1]))
    return lst


def random_string():
    def get_string():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(2, 50)))

    return [get_string() for _ in range(random.randint(3, 8))]


class ProgramTestCase(object):

    def __init__(self, path):
        with open(path, 'r') as f:
            contents = f.read()

        metadata_start = contents.index('/*') + 2
        metadata_end = contents.index('*/')
        metadata = json.loads(contents[metadata_start:metadata_end])

        self.name = metadata.get('test_name') or '.'.join(path.replace('.thing', '').split(os.sep)[-2:])
        self.code = contents[metadata_end + 2:]
        self.metadata = metadata
        self.target_path = path + 'c'