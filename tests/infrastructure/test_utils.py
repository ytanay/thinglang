import json
import os

from thinglang.lexer.lexical_analyzer import analyze_line
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser import parser
from thinglang.utils.source_context import SourceLine

INDENT = '\n' + ' ' * 8


def lexer_single(source: str, without_end: bool=False):
    return list(analyze_line(SourceLine.inline(source)))[:-1 if without_end else None]


def parse_local(code):
    tokens = lexer_single(code)
    vector = parser.collect_vectors(tokens)
    return vector.parse()


def validate_types(elements, types: list, descend_cls=None, descend_key=lambda x: x) -> None:
    assert len(elements) == len(types)

    for elem, expected_type in zip(elements, types):
        if descend_cls and isinstance(elem, descend_cls) and isinstance(expected_type, list):
            validate_types(descend_key(elem), expected_type, descend_cls, descend_key)
        else:
            assert isinstance(elem, expected_type)


def normalize_id(param):
    if isinstance(param, str):
        return Identifier(param)

    if isinstance(param, int):
        return NumericValue(param)

    if isinstance(param, (tuple, list)):
        return [normalize_id(x) for x in param]

    return param


class ProgramTestCase(object):

    def __init__(self, path):
        with open(path, 'r') as f:
            contents = f.read()

        metadata_start = contents.index('/*') + 2
        metadata_end = contents.index('*/')
        metadata_raw = contents[metadata_start:metadata_end]
        metadata = json.loads(metadata_raw)

        self.name = metadata.get('test_name') or ' '.join(path.replace('.thing', '').split(os.sep)[-2:])
        self.code = '\n' * (metadata_raw.count('\n') + 1) + contents[metadata_end + 2:]
        self.metadata = metadata
        self.target_path = path + 'c'
        self.source_path = path
