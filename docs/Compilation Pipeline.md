Compilation Pipeline
====================

A thinglang program goes through several steps on its road to becoming an executable, as outlined below:

### Lexical analysis
The thinglang source is first fed into the lexical analyzer, which emits streams of lexical tokens, delimited by lines in the original source.

Each lexical token contains contextual information about its origin in the code, which can be used to aid the diagnosis of parser and execution errors.

### Parsing
The parser inspects each stream of lexical tokens and attempts to reduce them into a single AST node, using the thinglang syntactic rules.

Each node is then attached to its parent based on indentation rules.

### Symbol generation
A symbol map is generated from each thing (i.e. class) definition, mapping the symbol names into descriptor objects. Symbol maps of external symbols (e.g. internal types, shared libraries, etc...) are also loaded and merged into a master map.

### Simplification
Certain constructs in the AST are modified to enable their compilation. For example, the inline list construct (`list lst = [1, 2, 3]`) is converted into a method call against the list's constructor, and subsequent pushes into the list.

### Indexing
Each local variable in the program is given a home in its containing stack frame. 

### Compilation
The finalized AST is traversed depth-first and bytecode instructions are emitted into a final executable stream.

The stream is combined with a static data stream (containing inline strings and numeric values) and debugging symbol information to produce the final thinglang executable format (THING/CC).

## Access conventions


### Primitive locals
```
number n = 5
Console.print(n)
n = 10
```

```
SET_STATIC idx(n) idx(5)
PUSH idx(n)
CALL_INTERNAL idx(Output) idx(write)
SET_STATIC idx(n) idx(10)
```

### Internal-type locals
```
text name = "andy"
name = name.uppercase()
Console.print(name + "says hello")
```

```
SET_STATIC idx(name) idx("andy")
PUSH idx(name)
CALL_INTERNAL idx(text) idx(uppercase)
SET idx(name)
PUSH_STATIC idx("says hello")
PUSH idx(name)
CALL idx(text) idx(+)
CALL idx(Output) idx(write)
```


### Chained references (arguments)
```
Person p = create Person("andy")
Console.print(p.info.name.upper())
```

```
PUSH_STATIC idx("andy")
CALL idx(Person) 0
SET idx(p)
PUSH idx(p)
RESOLVE idx(info)
RESOLVE idx(name)
CALL_INTERNAL idx(text) idx(uppercase)
CALL_INTERNAL idx(Output) idx(write)
```


### Chained references (assignments)

```
Person p = create Person("andy")
p.info.name = "andrew"
```

```
PUSH_STATIC idx("andy")
CALL idx(Person) 0
SET idx(p)
PUSH idx(p)
RESOLVE idx(info)
SET_MEMBER idx(name) idx("andrew")
```