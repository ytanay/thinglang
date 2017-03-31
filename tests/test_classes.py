from thinglang import run


def test_class_integration():
    assert run("""
thing Person
    has text name
    has number age

    created with name
        self.name = name
        self.age = 0

    does grow_up
        self.age = self.age + 1

    does say_hello with excitement_level
        Output.write("Hello from", self.name, ", who's ", self.age, "and is always up for a fun game of tag.")


thing Program
    setup
        text name = "yotam"
        text wants_to_grow_up = true
        #text name = Input.get_line("What is your name?")
        #text wants_to_grow_up = Input.get_line("Do you want to grow up?")
        Person person = create Person(name)

        if wants_to_grow_up
            person.grow_up()

        person.say_hello()
    """).output == """dog is dog"""

