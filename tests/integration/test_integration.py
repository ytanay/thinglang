import os
import pytest
import glob
import subprocess


from tests.infrastructure.test_utils import ProgramTestCase
from thinglang import pipeline
from thinglang.utils import logging_utils
from thinglang.utils.source_context import SourceContext

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

SEARCH_PATTERN = os.path.join(BASE_PATH, '**/*.thing')


def collect_tests():
    for path in glob.glob(SEARCH_PATTERN, recursive=True):
        #if 'nested_thing_access' in path:
            yield ProgramTestCase(path)


def split_lines(param):
    return param.replace('\r', '').split('\n')


@pytest.mark.parametrize('test_file', collect_tests(), ids=lambda x: x.name)
def test_thing_program(test_file: ProgramTestCase):
    expected_output = test_file.metadata['expected_output']
    test_input = bytes('\n'.join(test_file.metadata['input']) if 'input' in test_file.metadata else '', 'utf-8')
    bytecode = pipeline.compile(SourceContext.wrap(test_file.code))

    logging_utils.print_header('VM execution')

    with open(test_file.target_path, 'wb') as f:
        f.write(bytecode.bytes())

    vm = subprocess.Popen(["thinglang", test_file.target_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = (stream.decode('utf-8').strip() for stream in vm.communicate(test_input))
    print(stderr)

    logging_utils.print_header('VM output')
    print(stdout)

    if not isinstance(expected_output, str):
        stdout = split_lines(stdout)

    assert vm.returncode == 0, 'VM process crashed'
    assert stdout == expected_output, 'VM output did not match expected output'
