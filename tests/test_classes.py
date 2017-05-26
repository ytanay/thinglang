from unittest.mock import patch

import io

from thinglang import run


def test_class_integration():
    with patch('sys.stdin', io.StringIO('yotam\n19\n5')):
        assert run("""
thing Person
    has text name
    has number age

    setup with text name
        self.name = name

    does say_hello with number repeat_count
        number i = 0
        repeat while i < repeat_count
            Output.write("Hello number", i, "from", self.name, "who's", self.age, "years old and is always excited to get some coding done.")
            i = i + 1


thing Program
    setup
        Person person = create Person(Input.get_line("What is your name?"))
        number age = Input.get_line("What is your age?") as number

        if age
            person.age = age

        person.say_hello(Input.get_line("How excited are you?") as number)
    """).output == "What is your name?\nWhat is your age?\nHow excited are you?\n" +\
                   "\n".join("Hello number {} from yotam who's 19 years old and is always excited to get some coding done.".format(i) for i in range(5))

