# Virtual Functions

In order to support polymorphism, we need the ability to retain a reference to a per-instance table, via which we can jump to the correct procedure in the bytecode.

This requires the addition of a new opcode - `CALL_VIRTUAL`, which takes a single argument - the method ID. The runtime already processes types and methods in a fashion that is addressable by such  a tuple, so no significant changes are required there. In theory, any non-static and non-constructing call can be `CALL_VIRTUAL`, but we prefer only to use it when necessary, to save the overhead of dereferencing into the jump table. We will need to change the calling convention to push the _target_ of the method call after the arguments, so that it can be peeked by the runtime to determine the type ID.  

Also, since the regular `CALL` instruction includes both the address of the called procedure and the frame_size of the stack frame to allocate, we need a convention to initialize the stack frame of virtual functions.  We'll simply add this as metadata contained in the virtual jump table.
 
The virtual jump table is constructed while processing the code section of the bytecode. Class and method sentinels provide the necessary information to complete inheritance chains.

The goal is to use virtual calls only for non-static and non-constructing calls that refer to a type on a non-trivial inheritance chain (that is to say, a type that does not derive directly from object or that has classes deriving from it). If we encounter a method call to a *non* overridden method provided by the base `object` class, we'll use a virtual call for it, but all other calls related to that class should use standard `CALL`/`CALL_STATIC` opcodes.