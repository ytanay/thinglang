from thinglang import pipeline
from thinglang.lexer.values.identifier import Identifier
from thinglang.symbols.symbol import Symbol
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


def validate_member(member: Symbol, type, index, static=False):
    assert member.type == (Identifier(type) if isinstance(type, str) else type)
    assert member.index == index
    assert member.static is static

    assert member.kind is Symbol.MEMBER
    assert member.visibility is Symbol.PUBLIC


def validate_method(method: Symbol, type, arguments, index, static=False):
    assert method.type == (Identifier(type) if isinstance(type, str) else type), (method.type, type)
    assert method.index == index
    assert method.arguments == [Identifier(x) if isinstance(x, str) else x for x in arguments]
    assert method.static is static

    assert method.kind is Symbol.METHOD
    assert method.visibility is Symbol.PUBLIC


