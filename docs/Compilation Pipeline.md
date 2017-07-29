Compilation Pipeline
====================

A thinglang program goes through several steps on its road to becoming an executable. These steps are outlined in this document.

## Stages
### Lexical analysis
The thinglang source is first fed into the lexical analyzer, which emits a stream of lexical tokens, delimited by lines in the original source.

Each lexical token contains contextual information about its origin in the code, which can be used to aid the diagnosis of parser errors.

### Parsing
The parser inspects line-separated groups of lexical tokens and attempts to reduce them into a single AST node, which is then attached to its parent based on indentation rules.

### Symbol generation
A symbol map is generated from each ThingDefinition, mapping the symbol names into descriptor objects. At this point, any external referenced symbols are also loaded and merged into master map.

### Simplification
Certain constructs in the AST are "simplified" to aid compilation. For example, reference chains are converted into a series of assignment operations.

### Indexing
Each local variable in the program is given a home in its containing stack frame. 

### Compilation
The mutated AST is traversed depth-first and bytecode instructions are emitted into the final executable stream.

## Memory conventions


### Primitive locals
```
number n = 5
Output.write(n)
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
Output.write(name + "says hello")
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


### Chained references (arugments)
```
Person p = create Person("andy")
Output.write(p.info.name.upper())
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