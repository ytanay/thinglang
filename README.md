# thinglang
[![Build Status](https://travis-ci.org/ytanay/thinglang.svg?branch=master)](https://travis-ci.org/ytanay/thinglang)

Thinglang is a Python-inspired programming language, originally conceived as an educational project.

The syntax attempts to extract the core concepts of OOP into familiar terms and structures (i.e. meant to be explainable to an elementary school student reasonably easily). Put alternatively, the language as a whole is meant to motivate a clean  and consistent style of OOP. First things first, however - Hello World looks like this:
```cs
thing Program
    setup
        Console.print("hello world")
```

## Examples
An example of method calls:
```cs
thing Program
    setup 
        text name = "Andy"
        self.say_hello(name, 10)

    does say_hello with name, age
        Console.print("Hello from", age, "year old", name) # prints "Hello from 10 year old Andy"
```

Classes, methods, members and all that jazz:
```cs
thing Person
    has text name
    has number age

    setup with text name
        self.name = name

    does say_hello with number repeat_count
        for number i in 0..repeat_count
            Console.print("Hello number", i, "from", self.name, "who's", self.age, "years old and is always excited to get some coding done.")
            

thing Program
    setup
        Person person = create Person(Input.get_line("What is your name?"))
        number age = Console.read_line("What is your age?") as number
    
        if age not eq 0
            person.age = age
    
        person.say_hello(Input.get_line("How excited are you?") as number)
```

## General Overview
The original implementation of thinglang was written in pure Python as an exercise to learn about the components that make up a high level programming language and its runtime: lexical analysis, parsing, static analysis, compilation and execution. 

Since then, the runtime has been rewritten in C++, and the process now resembles that of the classic strictly typed languages, specifically Java/C#. Outlined below is the thinglang compilation pipeline. 

### Lexical Analysis + Parsing
The first time involves a line-by-line lexical tokenization process. A token stream from each line is transformed using multiple rounds of pattern replacements. Consider the line `if self.average([1, 2, 3]) eq 2`. The tokenizer will emit the following stream for this line: 
```
[L_IF L_SELF ACCESS ID(average) L_PAREN_OPEN L_BRACKET_OPEN NUMERIC(1) SEP NUMERIC(2) SEP NUMERIC(3) L_BRACKET_CLOSE L_PAREN_CLOSE L_EQ NUMERIC(2)]
```

What follows is the likely pattern transformation the stream will undergo:

```
[L_IF L_SELF ACCESS ID(average) L_PAREN_OPEN ListInitPartial([NUMERIC(1)]) SEP NUMERIC(2) SEP NUMERIC(3) L_BRACKET_CLOSE L_PAREN_CLOSE L_EQ NUMERIC(2)]
[L_IF L_SELF ACCESS ID(average) L_PAREN_OPEN ListInitPartial([NUMERIC(1), NUMERIC(2)]) SEP NUMERIC(3) L_BRACKET_CLOSE L_PAREN_CLOSE L_EQ NUMERIC(2)]
[L_IF L_SELF ACCESS ID(average) L_PAREN_OPEN ListInitPartial([NUMERIC(1), NUMERIC(2), NUMERIC(3)]) L_BRACKET_CLOSE L_PAREN_CLOSE L_EQ NUMERIC(2)]
[L_IF L_SELF ACCESS ID(average) L_PAREN_OPEN ListInit([NUMERIC(1), NUMERIC(2), NUMERIC(3)]) L_PAREN_CLOSE L_EQ NUMERIC(2)]
[L_IF L_SELF ACCESS ID(average) ArgListPartial([ListInit([NUMERIC(1), NUMERIC(2), NUMERIC(3)])]) L_PAREN_CLOSE L_EQ NUMERIC(2)]
[L_IF L_SELF ACCESS ID(average) ArgList([ListInit([NUMERIC(1), NUMERIC(2), NUMERIC(3)])]) L_EQ NUMERIC(2)]
[L_IF Access([L_SELF, ID(average)]) ArgList([ListInit([NUMERIC(1), NUMERIC(2), NUMERIC(3)])]) L_EQ NUMERIC(2)]
[L_IF MethodCall(target=[L_SELF, ID(average)], args=ArgList([ListInit([NUMERIC(1), NUMERIC(2), NUMERIC(3)])]) L_EQ NUMERIC(2)]
[L_IF LogicalOperation(lhs=MethodCall(target=[L_SELF, ID(average)], args=ArgList([ListInit([NUMERIC(1), NUMERIC(2), NUMERIC(3)])]), rhs=NUMERIC(2), type=EQ))]
[Conditional(LogicalOperation(lhs=MethodCall(target=[L_SELF, ID(average)], args=ArgList([ListInit([NUMERIC(1), NUMERIC(2), NUMERIC(3)])]), rhs=NUMERIC(2), type=EQ)))]
```

The object of this process is to reduce the token stream of a line to a single compound AST node. If at any point no transformations can be applied, and there is more than one element remaining from the original stream, the parser fails on the line. 

The output of the parser is an AST of compound nodes. Examples of nodes include method calls, assignments, conditionals, and so on. 


### Static Analysis
The AST undergoes two processes during SA: indexing and reduction. 

**Indexing** is a process which inspects decelerations, usage and assignment of every variable, instance, method, and member, and allocates an appropriate slot for it in its containing structure.


**Reduction** is a process in which compound nodes containing certain nested operations (e.g. nested method calls) are simplified into a series of non-compound nodes. This simplifies the logic which is required d compilation for certain constructs. 

### Symbol Generation 
A symbol map is generated from the AST, and its dependencies are inspected and loaded. If needed, additional source files go through the pipeline as described, otherwise, existing symbol maps are loaded. Processing continue once all dependencies are resolvd.

### Compilation 
The AST is traversed in DFS, each node in turn producing appropriate bytecode instructions. Since this process resolves and binds references, it is also catches non-syntatic errors. Additionally, static data is collected and debugging maps are generated for the final executable.

### Runtime 
With an executable in hand, we switch to the C++ runtime, which loads and processes the bytecode and its dependencies. Once ready, it begins an execution loop and performs its expected runtime duties (allocating memory, interacting with the system, catching error, and so on) 

### The Archives 

This is a description of the old Python-based execution model - it's slow, but still pretty nifty. 

Execution can begin after a bounded-reduced AST is created (see above)

The initialization sequence for any program goes roughly like this:
1. A program-global "heap" space is created, and first-order builtins are initialized inside it (currently, this means the `Input` and `Output` objects).
2. The *targets array* is created. The program is said to be executing as long as there are targets in the array. The program thus exits when there are no more targets, or when an error that the program cannot handle occurs.
3. The AST is scanned for a ThingDefinition with `name=Program` and an instance of it (`Thing<Program>`) is created. This instance is initially stored in an temporary (unreachable) location.
4. A root level stack frame is created, and contains a reference to the newly created `Thing<Program>` instance.
5. Every direct child of `MethodDefinition<constructor>` of `Thing<Program>` is copied into the *targets array*, and execution begins.

#### Pipeline
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
