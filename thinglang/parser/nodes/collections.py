from thinglang.foundation import definitions, templates
from thinglang.lexer.tokens import LexicalBinaryOperation
from thinglang.parser.nodes import BaseNode
from thinglang.parser.nodes.arithmetic import ArithmeticOperation


class ListInitialization(BaseNode):

    def __init__(self, slice=None):
        super(ListInitialization, self).__init__(slice if isinstance(slice, list) else [slice])

        if not slice:
            self.arguments = []
        elif isinstance(slice, list):
            self.arguments = slice
        else:
            self.arguments = [slice]

    def __iter__(self):
        return iter(self.arguments)

    def __len__(self):
        return len(self.arguments)

    def __getitem__(self, item):
        return self.arguments[item]

    def __setitem__(self, key, value):
        self.arguments[key] = value

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

        for arg in reversed(self.arguments):
            if arg.type in definitions.INTERNAL_TYPE_ORDERING:
                lines.append('\t\tauto {} = Program::argument<{}>();'.format(arg.transpile(), templates.format_internal_type(arg.type)))
            else:
                lines.append('\t\tauto {} = Program::pop();'.format(arg.transpile()))

        if not static:
            lines.append('\t\tauto self = Program::argument<this_type>();')

        return '\n'.join(lines) + '\n'
