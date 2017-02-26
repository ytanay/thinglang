import pytest

from tests.utils import generate_simple_output_program
from thinglang.runner import run


def test_empty_program():
    with pytest.raises(ValueError):
        run("")


def test_simple_output():
    assert run("""
thing Program
    does start
        Output.write("test")
    """).output == 'test'


TESTS = {
    'simple output': [
        ('Output.write("test")', 'test'),
        ('Output.write("hello world")', 'hello world'),
        ('Output.write("hello + world!")', 'hello + world!')
    ],
    'simple arithmetic': [
        ('Output.write(2 + 8)', '10'),
        ('Output.write(42 - 2)', '40'),
        ('Output.write(7 * 9)', '63'),
        ('Output.write(5 / 2)', '2.5')
    ],
    'order of operations': [
        ('Output.write(2 + 8 + 3)', '13'),
        ('Output.write(42 - 2 + 5)', '45'),
        ('Output.write(7 * 9 + 5)', '68'),
        ('Output.write(5 + 7 * 9)', '68')
    ],
    'method local stack + resolution': [
        (['number n = 5', 'Output.write(n)'], '5'),
        (['number n = 4', 'number m = 6', 'Output.write(n + m + 2)'], '12'),
        (['number n = 4', 'n = 7', 'Output.write(n)'], '7'),
        (['number n = 4', 'number n = 7', 'Output.write(n)'], AssertionError)
    ]
}


def flatten_dict(dct):
    lst = []
    for name, groups in list(dct.items()):
        for idx, group in enumerate(groups):
            lst.append(('{} #{}'.format(name, idx + 1), group[0], group[1]))
    return lst


@pytest.mark.parametrize('test_case', flatten_dict(TESTS), ids=lambda x: x[0])
def test_base_operations(test_case):
    print((generate_simple_output_program(test_case[1])))

    if isinstance(test_case[2], str):
        assert run(generate_simple_output_program(test_case[1])).output == test_case[2]
    else:
        with pytest.raises(test_case[2]):
            run(generate_simple_output_program(test_case[1]))