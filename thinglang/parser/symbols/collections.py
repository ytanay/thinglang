import itertools

from thinglang.foundation import Foundation
from thinglang.lexer.tokens import LexicalBinaryOperation
from thinglang.lexer.tokens.base import LexicalParenthesesOpen, LexicalParenthesesClose
from thinglang.parser.symbols import BaseSymbol
from thinglang.parser.symbols.arithmetic import ArithmeticOperation
from thinglang.utils.type_descriptors import ReplaceableArguments


class ListInitializationPartial(BaseSymbol):
    STRICTLY_TYPED = False

    def __init__(self, slice):
        super(ListInitializationPartial, self).__init__(slice)
        if len(slice) == 3 and isinstance(slice[1], LexicalBinaryOperation):
            self.value = slice[0].value[:-1] + [ArithmeticOperation([slice[0][-1]] + slice[1:])]
            return

        if self.STRICTLY_TYPED:
            slice[-2].type = "type"
            slice[-1].type = slice[-2]

        if isinstance(slice[0], ListInitializationPartial):
            self.value = slice[0].value + [slice[-1]]
        else:
            self.value = [slice[-1]]

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]


class ListInitialization(BaseSymbol, ReplaceableArguments):

    def __init__(self, slice=None):
        super(ListInitialization, self).__init__(slice)

        if not slice or len(slice) == 2 and isinstance(slice[0], LexicalParenthesesOpen) and isinstance(slice[1], LexicalParenthesesClose):
            self.arguments = []
        elif isinstance(slice[0], ListInitializationPartial):
            self.arguments = slice[0].value
        else:
            self.arguments = slice

    def __iter__(self):
        return iter(self.arguments)

    def __len__(self):
        return len(self.arguments)

    def __getitem__(self, item):
        return self.arguments[item]

    def evaluate(self, resolver):
        return [value.evaluate(resolver) for value in self.arguments]

    def describe(self):
        return self.arguments

    def statics(self):
        return [x for x in self.arguments if x.STATIC]

    def transpile(self, definition=False, pops=False, static=False):

        if not pops:
            return ', '.join(f'{x.type.transpile() + " " if definition else ""}{x.transpile()}' for x in self.arguments)

        lines = []

        if not static:
            lines.append('\t\tauto self = Program::argument<this_type>();')

        for arg in self.arguments:
            if arg.type in Foundation.INTERNAL_TYPE_ORDERING:
                lines.append('\t\tauto {} = Program::argument<{}>();'.format(arg.transpile(), Foundation.format_internal_type(arg.type)))
            else:
                lines.append('\t\tauto {} = Program::pop();'.format(arg.transpile()))

        return '\n'.join(lines) + '\n'
