# thinglang

Thinglang is a simple Python-like language I'm toying around with to get some experience on how a parser/compiler pair might be written using a high level language (surprise - the high level language I've chosen is Python!)

The syntax is modeled as something that might be explainable to a five year old reasonably easily. Hello World looks like this:
```
thing Program
    does start
        Output.write("hello world")
```

A more involved example might look something like this:
```
thing Program
    does start
        name = "Andy"
        age = 5
        self.say_hello(name, age)

    does say_hello with name, age
        Output.write("Hello from ", age, "year old", name) # prints "Hello from 5 year old andy"
```

This next example doesn't compile yet, but it's not (too) far away.
```
thing Person
    has name, age

    created with name
        self.name = name
        self.age = 0

    does grow_up
        self.age = self.age + 1

    does say_hello with excitement_level
        Output.write("Hello from", self.name, ", who's ", self.age, "and is always up for a fun game of tag.")

thing Program
    does start
        name = Input.ask("What is your name?")
        wants_to_grow_up = Input.ask("Do you want to grow up?") as boolean
        person = create Person(name)

        if wants_to_grow_up
            person.grow_up()

        person.say_hello()
```