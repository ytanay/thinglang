import pytest

from thinglang.runner import run


def test_zero_arg_function_calls():
    assert run("""
thing Program
    does start
        number n = 1
        number m = 2
        Output.write("before n=", n, " m=", m)
        self.say_hello()
        Output.write("after n=", n, " m=", m)

    does say_hello
        number n = 3
        Output.write("hello", n)
    """).output == """
before n= 1  m= 2
hello 3
after n= 1  m= 2
    """.strip()


def test_function_return_values():
    assert run("""
thing Program
    does start
        number result = self.say_hello()
        Output.write(result)
    does say_hello
        return 42
    """).output == """42""".strip()


def test_multi_arg_function_calls():
    assert run("""
thing Program
    does start
        text name = "Andy"
        number age = 10
        self.say_hello(name, age)
        self.say_hello("Yotam", 19)

    does say_hello with name, age
        Output.write("Hello from", age, "year old", name) # prints "Hello from 10 year old Andy"

    """).output == """
Hello from 10 year old Andy
Hello from 19 year old Yotam
    """.strip()


def test_function_call_integration():
    assert run("""
    thing Program
        does start
            number a = 15
            number b = self.add(a, 10)
            Output.write(a, b)
        does add with a, b
            return a + b
        """).output == """15 25""".strip()


def test_early_exit():
    assert run("""
    thing Program
        does start
            number a = 15
            number b = self.add_or_multiply(a, 10)
            Output.write(a, b)
        does add_or_multiply with a, b
            return a * b
            Output.write("never should appear")
            return a + b
        """).output == """15 150""".strip()


def test_chained_calls():
    assert run("""
    thing Program
        does start
            Output.write(self.get_7(), self.get_13())
            number res = self.mul(self.get_13(), self.add(self.get_7(), self.get_7()))
            Output.write(res)
            Output.write(self.mul(self.get_13(), self.add(self.get_7(), self.get_7())))
            Output.write(self.mul(self.add(self.get_7(), self.get_13()), res))

        does add with a, b
            return a + b

        does mul with a, b
            return a * b

        does get_7
            return 7

        does get_13
            return 13
        """).output == """7 13\n182\n182\n3640""".strip()


def test_arithmetic_over_method_calls():
    assert run("""
    thing Program
        does start
            number inter = self.get_13() + self.get_7() + self.get_7() * 3
            Output.write(inter, self.get_7() + self.get_13(), 2 * inter * self.get_7())

        does get_7
            return 7

        does get_13
            return 13
        """).output == """41 20 574""".strip()


def test_recursion():
    assert run("""
    thing Program
        does start
            Output.write(self.factorial(10))

        does factorial with n
            if n eq 1
                return 1
            number val = n * self.factorial(n-1)
            return val

        """).output == """3628800""".strip()