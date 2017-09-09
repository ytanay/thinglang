from thinglang.compiler.context import CompilationContext
from thinglang.compiler.opcodes import OpcodePushNull, OpcodeInstantiate
from thinglang.compiler.sentinels import SentinelThingDefinition
from thinglang.foundation import templates
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.lexer.tokens.functions import LexicalDeclarationConstructor, LexicalDeclarationReturnType
from thinglang.parser.nodes import DefinitionPairNode, BaseNode
from thinglang.parser.nodes.functions import ArgumentList, ReturnStatement
from thinglang.symbols.symbol import Symbol


class ThingDefinition(DefinitionPairNode):

    def describe(self):
        return self.name

    def transpile(self):
        type_cls_name, instance_cls_name = templates.get_names(self.name)
        return templates.FOUNDATION_TYPE.format(
            type_cls_name=type_cls_name, instance_cls_name=instance_cls_name,
            member_list=templates.format_member_list(self.members()),
            method_list=templates.format_method_list(self.methods()),
            members=self.transpile_children(indent=0, children_override=self.members()),
            methods=self.transpile_children(indent=0, children_override=self.methods())
        )

    def members(self):
        return [x for x in self.children if x.implements(MemberDefinition)]

    def methods(self):
        return [x for x in self.children if x.implements(MethodDefinition)]

    def compile(self, context: CompilationContext):
        context.append(SentinelThingDefinition(len(self.members()), len(self.methods())), self.source_ref)
        super().compile(context)


class MethodDefinition(BaseNode):

    def __init__(self, slice):
        super(MethodDefinition, self).__init__(slice)

        self.arguments = None
        self.return_type = None
        self.index = None
        self.static = False
        self.locals = None

        if isinstance(slice[0], LexicalDeclarationConstructor):
            self.name = LexicalIdentifier.constructor()
            if len(slice) > 1:
                self.arguments = slice[1]
        else:
            self.name = slice[1]
            self.static = slice[0].static_member

            if len(slice) > 2:
                if isinstance(slice[2], LexicalDeclarationReturnType):
                    self.return_type = slice[3]
                else:
                    self.arguments = ArgumentList(slice[2])

            if len(slice) > 4:
                self.return_type = slice[4]

        if not isinstance(self.arguments, ArgumentList):
            self.arguments = ArgumentList()

    def is_constructor(self):
        return self.name == LexicalIdentifier.constructor()

    def describe(self):
        return '{}, args={}'.format(self.name, self.arguments)

    def transpile(self):
        return templates.FOUNDATION_METHOD.format(
            name=(self.parent.name if self.is_constructor() else self.name).transpile(),
            return_type='Thing' if not self.is_constructor() else '',
            arguments='',  # Popped directly from stack
            preamble=self.arguments.transpile(static=self.static),
            body=self.transpile_children(2, self.children + [ReturnStatement([])])
        )

    def compile(self, context: CompilationContext):
        context.method_start(self.locals, self.frame_size, self.argument_count)

        if self.is_constructor():
            context.append(OpcodeInstantiate(context.symbols.index(self.parent)), self.source_ref)

        super(MethodDefinition, self).compile(context)

        if not self.is_constructor() and not self.children[-1].implements(ReturnStatement):
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

    def update_locals(self, locals):
        self.locals = locals


class MemberDefinition(BaseNode):
    def __init__(self, slice):
        super(MemberDefinition, self).__init__(slice)

        _, self.type, self.name = slice

    def describe(self):
        return 'has {} {}'.format(self.type, self.name)

    def transpile(self):
        return '{} {};'.format(self.type.transpile(), self.name.transpile())

    def symbol(self):
        return Symbol.member(self.name, self.type)

    def compile(self, context: CompilationContext):
        return
