from thinglang.thinglang import run


def test_simple_arrays():
    assert run("""
thing Program
    does start
        array names = ["yotam", "andrew", "john"]
        Output.write(names)

    """).output == """['yotam', 'andrew', 'john']"""


def test_array_initialization_over_function_calls():
    assert run("""
thing Program
    does start
        array numbers = self.build_array()
        Output.write(numbers)

    does get_10
        return 10

    does get_7
        return 7

    does add with a, b
        return a + b

    does build_array
        return [self.get_7(), self.get_10(), self.add(9, self.get_7() + self.get_10())]

    """).output == """[7, 10, 26]"""

