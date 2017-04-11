import pytest

from thinglang import run


def test_simple_loop():
    assert run("""
thing Program
    setup
        number i = 0
        repeat while i < 5
            Output.write("i =", i)
            i = i + 1
    """).output == """i = 0\ni = 1\ni = 2\ni = 3\ni = 4"""


def test_range_generator():
    assert run("""
thing Program
    setup
        Range i = create Range(0, 3)
        Output.write(i.next(), i.next(), i.next(), i.next(), i.next())
    """).output == """0 1 2 3 None"""


def test_range_generator_shortcut():
    assert run("""
thing Program
    setup
        Range i = 0..3
        Output.write(i.next(), i.next(), i.next(), i.next(), i.next())
    """).output == """0 1 2 3 None"""


def test_range_loop():
    assert run("""
    thing Program
        setup
            repeat for i in 0..4
                Output.write("i =", i)
        """).output == """i = 0\ni = 1\ni = 2\ni = 3"""
