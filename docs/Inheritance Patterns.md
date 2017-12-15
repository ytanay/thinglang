# Inheritance Patterns
thinglang supports 2 primary inheritance constructs - native inheritance and regular inheritance.

## Native Inheritance
When a user class inherits a native type (that is, a type which has the `internal` calling conventions), there is a bit of extra work.
 
 Although every thinglang instance in the runtime derives from a base instance type, it is illegal to move sideways between native and regular instances, since the calling conventions between the two differ radically. Therefore, in order to deal with this case, we add a new shadow member to the extending class, which can be accessed with the `super` keyword, and which has the type of the parent class (just as in the case of regular inheritance).

This shadow member can be instantiated by calling it in the scope of the extending class's constructor, e.g.
```python
thing Container extends map<K, V> with type K, type V
    setup with number max_size
        super()
```

This syntax is not allowed in other methods, not due to a technical consideration, but because it makes very little sense. There is however no prevention on calling the base constructor more than once.

TODO: should we enforce calling the base constructor before executing the extending constructor?