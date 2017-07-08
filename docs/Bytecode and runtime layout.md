# Bytecode & Runtime Layout

The thinglang bytecode is a lightweight language which operates over a state consisting of:
1. A method-local frame (a vector of Thing instances) - used for method locals - addressed using 32 bit pointers
2. A stack of Thing instances - used for method call arguments (and some computations)
3. A stack of frames - used for the call stack
4. A static data array (also a vector of Thing instances) - used for inlined strings, numeric values and user static data - addressed using 32 bit pointers
5. An internal type array - used for core internal types (text, number, Output, Input, etc...) and dynamically loaded native extensions - addressed using 32 bit internal pointers
6. A user type array - used for indexing types defined by the user (e.g. Program, Person, BankAccount, etc...) - addressed using 32 bit bytecode pointers


## Method calls

### Addressing schemes
The types of a thinglang program are indexed into 2 separate groups:
- *Internal addressing* - 32-bit unsigned integer - indexes internal types (runtime builtins and compiled native code)
- *Bytecode addressing* - 32-bit unsigned integer - indexes user defined types (i.e. types read from bytecode)

### Opcodes
#### CALL
Calls a user defined method (static or member) using bytecode addressing

**Arguments**:
1. Index of the type
2. Index of the method



```
p.say("Hello") # where p is an instance of Person
```

```
PUSH_STATIC  idx("hello")
PUSH         idx(p)
CALL         idx(Person) idx(say)
```
--------------------------------------------------
```
Post.is_valid_comment("<script>document.write(\"How 'bout that XSS?\")</script>")
```

```
PUSH_STATIC  idx(string above)
CALL         idx(Post) idx(is_valid_comment)
```

#### CALL_INTERNAL
Calls a compiled (native) method using native addressing

**Arguments**:
1. Index of the type
2. Index of the method

```
Ouput.write("hello world")
```

```
PUSH_STATIC      idx("hello world")
CALL_INTERNAL    idx(Output) idx(write)
```

