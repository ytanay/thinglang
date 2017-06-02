import collections
import io
import json

import os
import pytest
import glob
import subprocess

import thinglang
from thinglang import run, utils

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SEARCH_PATTERN = os.path.join(BASE_PATH, '**/*.thing')

TestCase = collections.namedtuple('TestCase', ['code', 'metadata', 'name', 'bytecode_target'])


def collect_tests():
    for path in glob.glob(SEARCH_PATTERN, recursive=True):
        with open(path, 'r') as f:
            contents = f.read()
            metadata_start = contents.index('/*') + 2
            metadata_end = contents.index('*/')
            metadata = json.loads(contents[metadata_start:metadata_end])
            yield TestCase(
                contents[metadata_end + 2:],
                metadata,
                metadata.get('test_name') or '.'.join(path.replace('.thing', '').split(os.sep)[-2:]),
                path + 'c'
            )


def split_lines(param):
    return param.replace('\r', '').split('\n')


@pytest.mark.parametrize('test_file', collect_tests(), ids=lambda x: x.name)
def test_thing_program(test_file):
    expected_output = test_file.metadata['expected_output']

    utils.print_header('Parsed AST')
    ast = thinglang.compiler(test_file.code)
    print(ast.tree())

    utils.print_header("Bytecode generation")
    bytecode = ast.compile().finalize()
    print(bytecode)

    utils.print_header('VM execution')

    with open(test_file.bytecode_target, 'wb') as f:
        f.write(bytecode)

    vm = subprocess.Popen(["thinglang", test_file.bytecode_target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = (stream.decode('utf-8').strip() for stream in vm.communicate())
    print(stderr)

    utils.print_header('VM output')
    print(stdout)

    local = thinglang.run(test_file.code).output

    if not isinstance(expected_output, str):
        stdout = split_lines(stdout)
        local = split_lines(local)

    assert vm.returncode == 0, 'VM process crashed'
    assert local == expected_output, 'Execution engine output did not match expected output'
    assert stdout == expected_output, 'VM output did not match expected output'




