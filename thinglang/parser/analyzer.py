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


def analyze(ast):
    analyze_method_resolution(ast)
    verify_method_definitions(ast)
    verify_thing_definitions(ast)
