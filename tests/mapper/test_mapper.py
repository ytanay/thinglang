from thinglang import pipeline
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils.source_context import SourceContext
from thinglang.lexer.values.identifier import Identifier
from thinglang.symbols.symbol import Symbol

source = """

thing Location
    has number x
    has number y
    
    setup
        self.x = 0
        self.y = 0
        
    static does distance with Location a, Location b returns number
        return math.square_root(math.square(a.x - b.x) + math.square(a.y - b.y))

thing Person
    has text name
    has number age
    has Location location
    
    setup with text name, number age
        self.name = name
        self.age = age
        
    does walk_to with Location new_location
        self.location = new_location
        
    does say_hello with text message
        Console.print("Message from " + self.name + ": " + message)
        
    does shout
        Console.print("Help!")
        
    
"""


def get_symbols(code):
    return SymbolMapper(pipeline.preprocess(SourceContext.wrap(code)))


def test_mapper_existence():
    symbols = get_symbols(source)
    assert all(Identifier(x) in symbols for x in ("Location", "Person"))


def test_member_symbol_description():
    symbols = get_symbols(source)
    person = symbols[Identifier('Person')]

    assert all(Identifier(x) in person for x in ("name", "age", "location", "walk_to", "say_hello", "shout"))

    name_desc = person[Identifier("name")]

    assert name_desc.kind is Symbol.MEMBER
    assert name_desc.type == Identifier("text")
    assert name_desc.visibility is Symbol.PUBLIC
    assert not name_desc.static
    assert name_desc.index == 0

    location_desc = person[Identifier("location")]
    assert location_desc.kind is Symbol.MEMBER
    assert location_desc.type == Identifier("Location")
    assert location_desc.visibility is Symbol.PUBLIC
    assert not location_desc.static
    assert location_desc.index == 2

    assert Identifier('x') in symbols[location_desc.type]


def test_method_symbol_description():
    symbols = get_symbols(source)
    person, location = symbols[Identifier('Person')], symbols[Identifier('Location')]

    walk_to = person[Identifier("walk_to")]
    assert walk_to.kind is Symbol.METHOD
    assert walk_to.type is None
    assert walk_to.arguments == [Identifier("Location")]
    assert not walk_to.static

    distance = location[Identifier('distance')]
    assert distance.kind is Symbol.METHOD
    assert distance.type == Identifier("number")
    assert distance.arguments == [Identifier("Location")] * 2
    assert distance.static

