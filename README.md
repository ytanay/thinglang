# thinglang
[![Build Status](https://travis-ci.org/ytanay/thinglang.svg?branch=master)](https://travis-ci.org/ytanay/thinglang)

Thinglang is a Python-inspired language I'm toying around with to get some experience on how a parser/compiler pair might be written using a high level language (surprise - the high level language I've chosen is Python!)

The syntax is modeled as something that might be explainable to an elementary school student reasonably easily. Hello World looks like this:
```cs
thing Program
    does start
        Output.write("hello world")
```

## Examples
An example of method calls:
```cs
thing Program
    does start
        text name = "Andy"
        self.say_hello(name, 10)

    does say_hello with name, age
        Output.write("Hello from", age, "year old", name) # prints "Hello from 10 year old Andy"
```

Class initialization, member definitions and all that jazz:
```cs
thing Person
    has text name
    has number age

    setup with name
        self.name = name

    does say_hello with repeat_count
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
```


## Static Analysis
The static analyzer takes the AST created by the parser and performs a number of checks and transformations which result in what thinglang calls a bounded-reduced AST. 

**Bounding** is the process which takes every general-case deceleration, lookup and assignment of every variable, instance, method, and member, and resolves it such that a direct link is attached between the definition and every subsequent reference. During this process, the AST is implcitly validated and any unresolved references trigger an appropriate error.


When type checking is implemented (soon?), bounding will also verify the type integrity of every reference.

**Reduction** is the process by which nodes containing certain nested operations (e.g. nested method calls) are simplified into a series of assignment operations. For example:
```cs
number val = f(g(), h(), i(j(), k()))
```
Is transformed into:
```cs
Transient<number> t0 = j()
Transient<number> t1 = k()
Transient<number> t2 = i(t0, t1)
Transient<number> t3 = g()
Transient<number> t4 = h()
Transient<number> t5 = f(t3, t4, t2)
```

## Execution Model

### Preamble
Execution can begin after a bounded-reduced AST is created (see above; this AST can generally be directly represented as thinglang bytecode, and should be thought of this way).

The initialization sequence for any program goes roughly like this:
1. A program-global "heap" space is created, and first-order builtins are initialized inside it (currently, this means the `Input` and `Output` objects).
2. The *targets array* is created. The program is said to be executing as long as there are targets in the array. The program thus exits when there are no more targets, or when an error that the program cannot handle occurs.
3. The AST is scanned for a ThingDefinition with `name=Program` and an instance of it (`Thing<Program>`) is created. This instance is initially stored in an temporary (unreachable) location.
4. A root level stack frame is created, and contains a reference to the newly created `Thing<Program>` instance.
5. Every direct child of `MethodDefinition<constructor>` of `Thing<Program>` is copied into the *targets array*, and execution begins.

### Execution pipeline
Every iteration of the execution pipeline beings by popping of a target from the beginning of the *targets array*. Examples of execution targets include instances of `AssignmentOperation`, `MethodCall`, `Conditional`, `Loop`, and even `ReturnStatement`s.

While a target is processed it can (and frequently does) affect the *targets array*. For example, a `Conditional` will copy its direct children in the positive branch to the *targets array* if its condition is evaluated as `true`, or the its direct children in the negative (i.e. "else") branch if its condition is evaluated as `false`. A `Loop` will copy its direct children **and itself** to the *targets array* if its condition evaluates as true (this is what makes it loop).

We'll look at a few examples of more intricate execution targets below.

#### Method calls
Method calls involve a bit of extra handholding. Described below is the general procedure for executing most method calls (the procedure for instance construction - i.e. creating a new `Thing` instance - is a bit different, and will be described seperately):

1. The target instance is looked up, first on the stack, then on the heap.
2. The method is looked up on the target instance.
3. A new stack frame is generated, and contains a reference to the target instance.
4. Arguments passed as part of the method call are copied (by reference, generally) into the new stack frame.
5. A stack frame terminator is generated, and optionally, contains the ID of the variable to which the result of the method call should be assigned (if the method call was caused by an `AssignmentOperation`).
6. The direct children of the method and the stack frame terminator are copied to the beginning of the *targets array*.
7. Execution proceeds normally, except;
    1. If a return statement is encountered, the return value is attached to the method's stack frame, and every target in the *targets array* until the stack frame terminator is removed.
8. When the stack frame terminator is encountered again, the called method's stack frame is popped off the stack.
    1. If the called method's stack frame contains a return value, it is assigned to the variable indicated by the terminator.
9. Execution proceeds normally.
