from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeInstantiate, OpcodePushNull
from thinglang.foundation import templates
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationMethod
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.definitions.tags import LexicalDeclarationConstructor, LexicalDeclarationReturnType, \
    LexicalDeclarationStatic
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.errors import VectorReductionError
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.statements.return_statement import ReturnStatement
from thinglang.parser.values.binary_operation import BinaryOperation
from thinglang.symbols.symbol import Symbol
from thinglang.utils.source_context import SourceReference
from thinglang.utils.type_descriptors import TypeList


class MethodDefinition(BaseNode):

    def __init__(self, name, arguments=None, return_type=None, static=False, token=None):
        super(MethodDefinition, self).__init__([name, arguments, return_type, static, token])

        self.name, self.arguments, self._return_type, self.static = name, (arguments or ArgumentList()), return_type, static

        self.index = None
        self.locals = None

    def is_constructor(self):
        return self.name == Identifier.constructor()

    def describe(self):
        return '{}, args={}'.format(self.name, self.arguments)

    def transpile(self):
        type_cls_name, instance_cls_name = self.container_name

        if self.is_constructor() and not self.children:
            return templates.IMPLICIT_CONSTRUCTOR.format(
                type_cls_name=type_cls_name,
                instance_cls_name=instance_cls_name
            )

        return templates.FOUNDATION_METHOD.format(
            name=(self.parent.name if self.is_constructor() else self.name).transpile(),
            class_name=type_cls_name,
            return_type='Thing' if not self.is_constructor() else '',
            arguments='',  # Popped directly from stack
            preamble=self.arguments.transpile(instance_cls_name, static=self.static),
            body=self.transpile_children(2, self.children + [ReturnStatement([])])
        )

    def compile(self, context: CompilationContext):
        context.method_start(self.locals, self.frame_size, self.argument_count)

        if self.is_constructor():
            context.append(OpcodeInstantiate(context.symbols.index(self.parent)), self.source_ref)

        super(MethodDefinition, self).compile(context)

        if not self.is_constructor() and not self.children[-1].implements(ReturnStatement) and self.return_type is not None:
            context.append(OpcodePushNull(), self.source_ref)

        context.method_end()

    def symbol(self):
        return Symbol.method(self.name, self.return_type, self.static, self.arguments)

    @property
    def frame_size(self):
        return len(self.locals)

    @property
    def argument_count(self):
        return len(self.arguments) + (0 if self.is_constructor() else 1)

    @property
    def return_type(self):
        if self.is_constructor():
            return self.parent.name
        return self._return_type

    def update_locals(self, locals):
        self.locals = locals

    @classmethod
    def empty_constructor(cls, parent):
        instance = MethodDefinition(Identifier.constructor(), token=SourceReference.generated('implicit constructor'))
        instance.parent = parent
        return instance

    # Parser rules

    METHOD_NAME_TYPES = (Identifier,) + tuple(BinaryOperation.OPERATIONS.keys())

    @staticmethod
    @ParserRule.mark
    def method_definition(_1: LexicalDeclarationMethod, name: METHOD_NAME_TYPES):
        return MethodDefinition(name)

    @staticmethod
    @ParserRule.mark
    def constructor_definition(_1: LexicalDeclarationConstructor):
        return MethodDefinition(Identifier.constructor(), token=_1)

    @staticmethod
    @ParserRule.mark
    def add_return_type(method: 'MethodDefinition', _2: LexicalDeclarationReturnType, return_type: Identifier):
        if method._return_type is not None:
            raise VectorReductionError('Duplicate return type declaration')
        method._return_type = return_type
        return method

    @staticmethod
    @ParserRule.mark
    def add_arguments(method: 'MethodDefinition', arguments: TypeList):
        if method._return_type is not None:
            raise VectorReductionError('Argument list must come before return type')
        method.arguments = ArgumentList(arguments)
        return method

    @staticmethod
    @ParserRule.mark
    def tag_static(_: LexicalDeclarationStatic, method: 'MethodDefinition'):
        method.static = True
        return method
