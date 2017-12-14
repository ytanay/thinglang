# Pipeline Overview
The original implementation of thinglang was written in pure Python as an exercise to learn about the components that make up a high level programming language and its runtime: lexical analysis, parsing, static analysis, compilation and execution. 

Since then, the runtime has been rewritten in C++, and the process now resembles that of the classic strictly typed languages, specifically Java/C#. Outlined below is the thinglang compilation pipeline. 

## Lexical Analysis + Parsing
The first stage is a line-by-line lexical tokenization process. Each time stream (one per line) is transformed using multiple rounds of pattern replacements. Consider the line `if self.average([1, 2, 3]) eq 2`. The tokenizer will emit the following stream for this line: 
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

## Static Analysis
The AST undergoes two processes during SA: indexing and reduction. 

**Indexing** is a process which inspects declarations, usages and assignments of variables, instances, methods, and members.  Each entity is given an appropriate slot in its containing structure.


**Reduction** is a process in which compound nodes containing certain nested operations (e.g. nested method calls) are simplified into a series of non-compound nodes. This simplifies the logic required during compilation for certain constructs. 

## Symbol Generation 
A symbol map is generated from the AST, and its dependencies are inspected and loaded. If needed, additional source files go through the pipeline as described, otherwise, existing symbol maps are loaded. Processing continues once all dependencies are resolved. 

## Compilation 
The AST is traversed in DFS, each node in turn producing appropriate bytecode instructions. Since this process resolves and binds references, it is also catches certain non-syntactic errors. Additionally, static data is collected and debugging maps are generated for the final executable if applicable. 

## Runtime 
With an executable in hand, we switch to the C++ runtime. After loading and processing the bytecode and its dependencies, it begins an execution loop and performs its expected runtime duties (allocating memory, interacting with the system, catching errors, and so on). 
