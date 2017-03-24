import os

import itertools
from collections import namedtuple

from thinglang.utils import flatten_list

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_EXPECTATION_INDICATOR = '# Output:'
TEST_CASE = namedtuple('TEST_CASE', ['name', 'group', 'source', 'expected_output'])

def read_case(group, file):
    with open(os.path.join(BASE_DIR, group, file)) as f:
        lines = f.readlines()

    header = list(itertools.takewhile(lambda x: x.startswith('# '), lines))
    assert header[0].strip() == OUTPUT_EXPECTATION_INDICATOR and all(x.startswith('# ') for x in header), 'Invalid output expectation header'

    expected_output = '\n'.join([x[2:] for x in header[1:]]).strip()
    source = ''.join(lines)

    return TEST_CASE(os.path.splitext(file)[0], group, source, expected_output)



def collect_test_cases():
    dirs = [x for x in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, x)) and not x.startswith('.')]
    files = [(dir, file) for dir in dirs for file in os.listdir(dir)]
    cases = [read_case(*file) for file in files]
    return cases

def pytest_generate_tests(metafunc):
    if 'source' in metafunc.fixturenames:
        cases = collect_test_cases()

        metafunc.parametrize("source", cases, ids=['{}.{}'.format(x.group, x.name) for x in cases])