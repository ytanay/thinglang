from thinglang import pipeline
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils.source_context import SourceContext

SOURCE_LOCATION = '''
thing Location
    has number x
    has number y
    
    setup
        self.x = 0
        self.y = 0
        
    static does distance with Location a, Location b returns number
        return math.square_root(math.square(a.x - b.x) + math.square(a.y - b.y))

'''

SOURCE_PAIR = '''
thing Pair with type T
    has T lhs
    has T rhs
    has list<T> parts
    has list<list<list<T>>> nested
    
    does set_values with T lhs, T rhs returns T
        self.lhs = lhs
        self.rhs = rhs
        return lhs + rhs
        
    does nested_param with list<T> input returns list<T>
        return input

'''

SOURCE_PERSON = '''
thing Person
    has text name
    has number age
    has Location location
    has Pair<number> favorite_numbers
    
    setup with text name, number age
        self.name = name
        self.age = age
        
    does walk_to with Location new_location
        self.location = new_location
        
    does say_hello with text message
        Console.print("Message from " + self.name + ": " + message)
        
    does shout
        Console.print("Help!")
        
'''

SOURCE_FULL = SOURCE_LOCATION + SOURCE_PERSON + SOURCE_PAIR


def get_symbols(code) -> SymbolMapper:
    return SymbolMapper(pipeline.preprocess(SourceContext.wrap(code)))
