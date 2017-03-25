from thinglang.thinglang import run


def test_simple_arrays():
    assert run("""
thing Program
    does start
        array names = ["yotam", "andrew", "john"]
        Output.write(names)

    """).output == """['yotam', 'andrew', 'john']"""

