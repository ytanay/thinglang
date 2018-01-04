# thinglang
[![Build Status](https://travis-ci.org/ytanay/thinglang.svg?branch=master)](https://travis-ci.org/ytanay/thinglang)

thinglang is a Python-inspired programming language, originally conceived as an educational project.

The syntax attempts to extract the core concepts of OOP into familiar terms and structures (i.e. meant to be explainable to an elementary school student reasonably easily). In a senetence, the primary aim of thinglang is to be as powerful (in the software engineering sense) and performant as Java/C#, but retain as much of the pleasent syntax of Python as possible. 

First things first, however - Hello World looks like this:
```python
thing Program
    setup
        Console.print("Hello, world!")
```

## Introduction
At its heart, thinglang closely follows the principles of classic strictly typed programming languages - namely, Java and C# - but attempts to expose a more "Pythonic" syntax on the surface.

Every thinglang program starts its execution at a thing class named `Program`. When the program starts, this class is instantiated, meaning that the first line of code that runs will be that of the `Program` constructor. In thinglang constructors are marked by the word `setup`.

```python
thing Program
    setup
        # This is the constructor of the Program class
        Console.print("Hello, world!")
```

As would be expected, almost everything in thinglang is an object, and consequently every line of code resides in a method, which is contained in a class. Let's look at a more comprehensive example:

```python
thing Person
    # Each of the following is a member of the Person class

    has text name
    has number age
    has Location current_location
    has list<Hobby> hobbies       # Defines a list of Hobby instances
    has map<text, Person> friends # Defines a map of text -> Person

    # This constructor takes 2 arguments, and sets the members of the Person class
    setup with text name, number age
        self.name = name
        self.age = age
        self.current_location = Location() # Creates a new instance of the Location class
        self.hobbies = list<Hobby>()       # Creates a new, empty list
        self.friends = map<text, Person>() # Creates a new, empty map

    # This defines a method that take no arguments and returns nothing
    does say_hello
        Console.print("Hello from {}", [self.name])

    # This method takes no arguments and returns a boolean value
    does is_home returns bool
        return self.current_location.name eq "home"

    # This method takes one argument of type string
    does add_hobby with text hobby_name
        self.hobbies.append(Hobby(hobby_name)) # We construct a new hobby object from the text object

    # This method shares the same name as the one above, but takes different arguments (i.e. is overloaded)
    does add_hobby with Hobby hobby
        self.hobbies.append(hobby)

    does perform_hobbies
        for Hobby hobby in self.hobbies # A simple iteration loop
            Console.print("Performing: {}", [self.name, hobby])
            try
                hobby.perform()
            handle HobbyException exc
                Console.print("Failed to perform hobby: {}", [exc])
```

### OOP constructs
thinglang supports the usual OOP suspects (inheritance, polymorphism, field visibility and generics). Here's a possible implementation for a generic LRU container type:

```python
thing LRUContainer with type K, type V extends map<K, LRUEntry<V>>
    has private number expirey_seconds
    
    setup with number expirey_seconds
        self.expirey_seconds = expirey_seconds
        
    does get with K key returns V
        LRUEntry<V> entry = self[K]
        if Time.now() - value.ts > self.expirey_seconds
            self.remove(K)
            return null
        else
            return entry.value
            
     does set with K key, V value
         self[K] = LRUEntry(value)

thing LRUEntry with type V
    has V value
    has Time ts
    
    setup with V value
        self.value = value
        self.ts = Time.now()
```

## Language Reference
thinglang's syntax is mostly complete, but it is still lacking a reasonable standard library (which is being slowly developed).

The current core types are as follows (each link points to the thinglang stub for the type):
- [`text`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/text.thing): the string type.
- [`number`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/number.thing): the integer type.
- [`list`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/list.thing): a generic, mutable random-access list.
- [`map`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/map.thing): a generic key to value container.
- [`iterator`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/iterator.thing): which is constructed from lists and maps.
- [`Exception`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/Exception.thing): the base exception classs.
- [`Console`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/Console.thing): for terminal based IO.
- [`File`](https://github.com/ytanay/thinglang/blob/master/thinglang/foundation/source/File.thing): read/write create files.

For more, see the various notes in the [docs](https://github.com/ytanay/thinglang/tree/master/docs) directory.
