import random
import string
from unittest.mock import patch

import io

import pytest

from tests.utils import random_string
from thinglang import utils
from thinglang.thinglang import run


def test_input_single_line():
    with patch('sys.stdin', io.StringIO('single input line')):
        assert run("""
thing Program
    does start
        text input = Input.get_line()
        Output.write("Input is:", input)
        """).output == "Input is: single input line"


def test_input_multiple_lines():
    with patch('sys.stdin', io.StringIO('first line\nsecond line')):
        assert run("""
thing Program
    does start
        text input = Input.get_line()
        Output.write("1:", input)
        Output.write("2:", Input.get_line())
        """).output == "1: first line\n2: second line"


def test_eof():
    with pytest.raises(EOFError), patch('sys.stdin', io.StringIO('')):
        assert run("""
thing Program
    does start
        Input.get_line()
        """)


def test_looped_reads():
    data = random_string()
    utils.print_header('Random data', data)
    with patch('sys.stdin', io.StringIO('\n'.join(data) + '\n\n')):
        assert run("""
thing Program
    does start
        text line = Input.get_line()
        number idx = 0
        repeat while line not eq ""
            Output.write(idx, line)
            line = Input.get_line()
            idx = idx + 1
        Output.write("Total:", idx)
        """).output == '\n'.join(['{} {}'.format(idx, line) for idx, line in enumerate(data)]) + '\nTotal: {}'.format(len(data))
