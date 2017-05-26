from thinglang import run, compiler


def test_bytecode_generation():
    with open('../thingc/resources/test_file.thingc', 'wb') as f:
        f.write(compiler("""
    thing Program
        setup
            number n = 10
            Output.write(n)
            n = 5
            Output.write(n)

            self.count()
            self.say_hello()

        does count# with number first
            Output.write("Counting")
            #Output.write(first)

        does say_hello
            Output.write("Hello")

        """).compile().finalize())