from thinglang.execution.errors import ReturnInConstructorError, EmptyMethodBody, EmptyThingDefinition, \
    ArgumentCountMismatch
from thinglang.parser.symbols.classes import MethodDefinition, ThingDefinition
from thinglang.parser.symbols.functions import ReturnStatement, MethodCall


def verify_method_definitions(ast):
    for child in ast.find(lambda x: isinstance(x, MethodDefinition)):
        if child.is_constructor() and list(child.find(lambda x: isinstance(x, ReturnStatement))):
            raise ReturnInConstructorError(child)

        if not child.children:
            raise EmptyMethodBody()


def verify_thing_definitions(ast):
    for child in ast.find(lambda x: isinstance(x, ThingDefinition)):
        if not child.children:
            raise EmptyThingDefinition()


def analyze_method_resolution(ast):
    for child in ast.find(MethodCall):
        if child.target[0].is_self():
            thing_definition = child.upwards(ThingDefinition)
        else:
            thing_definition = ast.find(ThingDefinition, lambda x: x.name == child.target[0], single=True)

        if thing_definition is None:
            print('Warning: method resolution cannot be validated!')
        elif len(child.arguments) != len(thing_definition.find(MethodDefinition, lambda x: x.name == child.target[1], single=True).arguments):
            raise ArgumentCountMismatch()


def analyze(ast):
    analyze_method_resolution(ast)
    verify_method_definitions(ast)
    verify_thing_definitions(ast)
