from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeInstantiate, OpcodePushNull, OpcodeReturn, OpcodeArgCopy
from thinglang.compiler.sentinels import SentinelMethodDefinition
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
from thinglang.symbols.symbol_map import SymbolMap
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
            name=self.name.transpile(),
            class_name=type_cls_name,
            return_type='Thing',
            arguments='',  # Popped directly from stack
            preamble=self.arguments.transpile(instance_cls_name, static=self.static, constructor=self.is_constructor()),
            body=self.transpile_children(2, self.children),
            epilogue=templates.RETURN_SELF if self.is_constructor() else templates.RETURN_NULL

        )

    def compile(self, context: CompilationBuffer):

        if self.is_constructor():
            context.append(OpcodeInstantiate(self.argument_count, context.symbols[self.parent.name].offset), self.source_ref)
        elif self.argument_count:
            context.append(OpcodeArgCopy(self.argument_count), self.source_ref)

        if self.children:
            super(MethodDefinition, self).compile(context)

        if not self.is_constructor() and not isinstance(self.children[-1], ReturnStatement) and self.return_type is not None:
            context.append(OpcodePushNull(), self.source_ref)

        if not isinstance(context.last_instruction, OpcodeReturn):
            context.append(OpcodeReturn(), self.source_ref)

        return context

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
        instance = MethodDefinition(Identifier.constructor()).deriving_from(parent)
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
