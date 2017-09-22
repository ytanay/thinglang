from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodeInstantiate, OpcodePushNull
from thinglang.foundation import templates
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationConstructor, LexicalDeclarationReturnType
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.statements.return_statement import ReturnStatement
from thinglang.symbols.symbol import Symbol
from thinglang.utils.source_context import SourceReference


class MethodDefinition(BaseNode):

    def __init__(self, slice):
        super(MethodDefinition, self).__init__(slice)

        self.arguments = None
        self._return_type = None
        self.index = None
        self.static = False
        self.locals = None

        if isinstance(slice[0], LexicalDeclarationConstructor):
            self.name = Identifier.constructor()
            if len(slice) > 1:
                self.arguments = slice[1]
        else:
            self.name = slice[1]
            self.static = slice[0].static_member

            if len(slice) > 2:
                if isinstance(slice[2], LexicalDeclarationReturnType):
                    self._return_type = slice[3]
                else:
                    self.arguments = ArgumentList(slice[2])

            if len(slice) > 4:
                self._return_type = slice[4]

        if not isinstance(self.arguments, ArgumentList):
            self.arguments = ArgumentList()

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
        instance = cls([LexicalDeclarationConstructor('setup', SourceReference.generated('implicit constructor'))])
        instance.parent = parent
        return instance
