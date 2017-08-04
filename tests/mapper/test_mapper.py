import thinglang
from thinglang import SymbolMapper
from thinglang.lexer.tokens.base import LexicalIdentifier
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
        Output.write("Message from " + self.name + ": " + message)
        
    does shout
        Output.write("Help!")
        
    
"""


def test_mapper_existence():
    ast = thinglang.preprocess(source)
    symbols = SymbolMapper(ast)
    assert all(LexicalIdentifier(x) in symbols for x in ("Location", "Person"))


def test_member_symbol_description():
    ast = thinglang.preprocess(source)
    symbols = SymbolMapper(ast)
    person = symbols[LexicalIdentifier('Person')]

    assert all(LexicalIdentifier(x) in person for x in ("name", "age", "location", "walk_to", "say_hello", "shout"))

    name_desc = person[LexicalIdentifier("name")]

    assert name_desc.kind is Symbol.MEMBER
    assert name_desc.type == LexicalIdentifier("text")
    assert name_desc.visibility is Symbol.PUBLIC
    assert not name_desc.static
    assert name_desc.index == 0

    location_desc = person[LexicalIdentifier("location")]
    assert location_desc.kind is Symbol.MEMBER
    assert location_desc.type == LexicalIdentifier("Location")
    assert location_desc.visibility is Symbol.PUBLIC
    assert not location_desc.static
    assert location_desc.index == 2

    assert LexicalIdentifier('x') in symbols[location_desc.type]


def test_method_symbol_description():
    ast, symbols = thinglang.preprocess(source)
    person, location = symbols[LexicalIdentifier('Person')], symbols[LexicalIdentifier('Location')]

    walk_to = person[LexicalIdentifier("walk_to")]
    assert walk_to.kind is Symbol.METHOD
    assert walk_to.type is None
    assert walk_to.arguments == [LexicalIdentifier("Location")]
    assert not walk_to.static

    distance = location[LexicalIdentifier('distance')]
    assert distance.kind is Symbol.METHOD
    assert distance.type == LexicalIdentifier("number")
    assert distance.arguments == [LexicalIdentifier("Location")] * 2
    assert distance.static

