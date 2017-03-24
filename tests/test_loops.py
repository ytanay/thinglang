from thinglang.runner import run


def test_simple_loop():
    assert run("""
thing Program
    does start
        number i = 0
        repeat while i < 5
            Output.write("i =", i)
    """).output == """i = 0\ni = 1\ni = 2\ni = 3\ni = 4"""
