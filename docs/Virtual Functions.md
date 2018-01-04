# Virtual Functions

In order to support polymorphism, we need the ability to retain a reference to a per-instance table, via which we can jump to the correct procedure in the bytecode.

This requires the addition of a new opcode - `CALL_VIRTUAL`, which takes a single argument - the method ID. The runtime already processes types and methods in a fashion that is addressable by such  a tuple, so no significant changes are required there. In theory, any non-static and non-constructing call can be `CALL_VIRTUAL`, but we prefer only to use it when necessary, to save the overhead of dereferencing into the jump table. We will need to change the calling convention to push the _target_ of the method call after the arguments, so that it can be peeked by the runtime to determine the type ID.  

Also, since the regular `CALL` instruction includes both the address of the called procedure and the frame_size of the stack frame to allocate, we need a convention to initialize the stack frame of virtual functions.  We'll simply add this as metadata contained in the virtual jump table.
 
The virtual jump table is constructed while processing the code section of the bytecode. Class and method sentinels provide the necessary information to complete inheritance chains.

## Required Common Methods

An interesting discussion that arises from this point is that of mandatory inheritance from a globally base `object` class. The thinglang philosophy would require that all objects have, at least in some capacity, methods to check for equality, represent the instance textually and derive a hash code from it. 
 
Java and C# enforce this, Python encourages it, and C++ couldn't care less. What would be the correct approach for thinglang?

### Implicit mandatory inheritance
Having all non-inheriting classes derive from a base `object` class, and declaring `does eq`, `as text`, `as hashcode` in that base class as Java and C# do is by all means an elegant approach. An additional (unrelated) attribute that it gives is allowing all types to be upcasted into `object` and later optionally downcasted back to their original type, enabling a rather unpleasant form of genericism, albeit one that makes a lot of sense for methods like `Console.print()`.

However, this comes at the cost of making many function calls virtual, since there is no reasonable way to statically determine during compilation what the runtime type of an object will be, except in a few specific cases. Furthermore, it is not clear how cleanly this fits in with the other desirable features, such as automatically generating these base methods when not explictly provided.

### Special-case commons compilation
Another, slightly dirtier approach is to explicitly mark a set of methods common to all objects (automatically generated if not provided). Then, during compilation, we select regular calls if the class is not part of any inheritance chain, and a virtual call if it is, or if the call is to one of these common methods.
 
This is slightly more optimized, but doesn't back up these common methods by an explicit contract, which is pretty terrible.
 
### Selected approach
When compiling a method, we'll perform the following logic:
#### Candidate selection
1. If there is a single symbol that matches the exact argument types given, it is selected as the target symbol.
2. Otherwise, if there is a single symbol that matches the argument types (by cast, if need), it is selected as the target symbol.
3. If neither holds, no valid target exists

### Calling convention selection
1. If the symbol is defined in any base class, or is overridden in any child class, the call will be virtual.
2. Otherwise, the call will be direct.