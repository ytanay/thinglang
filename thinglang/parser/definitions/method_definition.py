from thinglang.compiler.buffer import CompilationBuffer
from thinglang.compiler.opcodes import OpcodeInstantiate, OpcodePushNull, OpcodeReturn, OpcodeArgCopy
from thinglang.lexer.definitions.tags import LexicalDeclarationConstructor, LexicalDeclarationReturnType, \
    LexicalDeclarationStatic
from thinglang.lexer.definitions.thing_definition import LexicalDeclarationMethod
from thinglang.lexer.operators.binary import LexicalBinaryOperation
from thinglang.lexer.operators.casts import LexicalCast
from thinglang.lexer.operators.comparison import LexicalComparison
from thinglang.lexer.values.identifier import Identifier, GenericIdentifier
from thinglang.parser.constructs.cast_operation import CastTag
from thinglang.parser.definitions.argument_list import ArgumentList
from thinglang.parser.errors import VectorReductionError
from thinglang.parser.nodes.base_node import BaseNode
from thinglang.parser.rule import ParserRule
from thinglang.parser.statements.assignment_operation import AssignmentOperation
from thinglang.parser.statements.return_statement import ReturnStatement
from thinglang.parser.values.method_call import MethodCall
from thinglang.parser.values.named_access import NamedAccess
from thinglang.symbols.inline_candidate import InlineCandidate
from thinglang.symbols.symbol import Symbol
from thinglang.utils.type_descriptors import TypeList


class MethodDefinition(BaseNode):
    """
    A method definition
    Must be a direct child of a ThingDefinition
    """

    def __init__(self, name, arguments=None, return_type=None, static=False, token=None):
        super(MethodDefinition, self).__init__([name, arguments, return_type, static, token])

        self.name, self.arguments, self._return_type, self.static = name, (arguments or ArgumentList()), return_type, static

        self.index = None
        self.locals = None

    def __repr__(self):
        return 'does {}{}'.format(self.name, f' with {self.arguments}' if self.arguments else '')

    def is_constructor(self):
        return self.name == Identifier.constructor()

    def compile(self, context: CompilationBuffer):

        if self.is_constructor():
            context.append(OpcodeInstantiate(context.symbols.index(context.symbols[self.parent.name]), self.argument_count), self.source_ref)
        elif self.argument_count:
            context.append(OpcodeArgCopy(self.argument_count, int(not self.is_constructor())), self.source_ref)

        if self.children:
            super(MethodDefinition, self).compile(context)

        if not self.is_constructor() and not isinstance(self.children[-1], ReturnStatement) and self.return_type is not None:
            context.append(OpcodePushNull(), self.source_ref)

        if not isinstance(context.last_instruction, OpcodeReturn):
            context.append(OpcodeReturn(), self.source_ref)

        return context

    def finalize(self):
        if not self.is_constructor():
            return super().finalize()

        for descendant in self.descendants:
            if isinstance(descendant, MethodCall) and descendant.target[0] == Identifier.super():
                descendant.replace(AssignmentOperation(
                    AssignmentOperation.REASSIGNMENT,
                    NamedAccess([Identifier.self(), Identifier.super()]),
                    MethodCall(NamedAccess([self.parent.extends, Identifier.constructor()]), descendant.arguments, is_captured=True).deriving_from(self)
                ).deriving_from(descendant))

        super().finalize()

    def symbol(self):
        return Symbol.method(self.name, self.return_type, self.static, self.arguments, node=InlineCandidate.from_method(self))

    @property
    def frame_size(self):
        return len(self.locals)

    @property
    def argument_count(self):
        return len(self.arguments)

    @property
    def explicit_local_count(self): # TODO: does this include self?
        return self.frame_size - self.argument_count

    @property
    def return_type(self):
        if self.is_constructor():
            if self.parent.generics:
                return GenericIdentifier(self.parent.name, tuple(self.parent.generics))
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

    METHOD_NAME_TYPES = (Identifier, LexicalComparison, LexicalBinaryOperation)

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
            raise VectorReductionError('Duplicate return type declaration', [method, return_type])
        if method.is_constructor():
            raise VectorReductionError('Constructors cannot have a return type', [method, return_type])
        method._return_type = return_type
        return method

    @staticmethod
    @ParserRule.mark
    def add_arguments(method: 'MethodDefinition', arguments: TypeList):
        if method._return_type is not None:
            raise VectorReductionError('Argument list must come before return type', [method, arguments])
        method.arguments = ArgumentList(arguments)
        return method

    @staticmethod
    @ParserRule.mark
    def tag_static(_: LexicalDeclarationStatic, method: 'MethodDefinition'):
        method.static = True
        return method

    @staticmethod
    @ParserRule.predicate(lambda tokens, index: index == 0)
    def parse_casting_method(_: LexicalCast, return_type: Identifier):
        return MethodDefinition(CastTag(return_type), return_type=return_type)
