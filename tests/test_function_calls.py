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


def test_multi_arg_function_calls():
    assert run("""
thing Program
    does start
        text arg_val = "some value"
        self.say_hello(1, "hello", arg_val)

    does say_hello with arg1, arg2, arg3
        Output.write("in say_hello", arg1, arg2, arg3)
    """).output == """
in say_hello 1 hello some value
    """.strip()