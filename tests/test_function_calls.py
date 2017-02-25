from thinglang.runner import run


def test_function_calls():
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