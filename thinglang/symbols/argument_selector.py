import collections
import copy

from thinglang.compiler.errors import NoMatchingOverload
from thinglang.lexer.values.identifier import Identifier

SymbolOption = collections.namedtuple('SymbolOption', ['symbol', 'remaining_arguments'])


class ArgumentSelector(object):
    """
    Aids in disambiguating overloaded method symbols contained in MergedSymbol objects.
    Managed state regarding arguments already observed, and filters out overloads and all arguments are processed.
    If a matching overload exists, it is returned - otherwise, an exception is thrown.
    """

    def __init__(self, symbols):
        self.symbols = symbols
        self.collected_arguments = []
        self.options = [SymbolOption(symbol, copy.deepcopy(symbol.arguments)) for symbol in symbols]

    def constraint(self, resolved):
        """
        Filters out option groups that do not expect to see the resolved type as their next argument
        """
        self.collected_arguments.append(resolved)

        new_options = []

        for option in self.options:
            if option.remaining_arguments and self.type_match(resolved, option.remaining_arguments.pop(0)):
                new_options.append(option)

        self.options = new_options

        if not self.options:
            raise NoMatchingOverload(self.symbols, self.collected_arguments)

    def disambiguate(self):
        """
        Selects the best matching overload
        """
        option_group = [option for option in self.options if not option.remaining_arguments]

        if len(option_group) != 1:
            raise NoMatchingOverload(self.symbols, self.collected_arguments)

        return option_group[0].symbol

    @staticmethod
    def type_match(resolved, expected_type):
        """
        Checks if two types match (TODO: take inheritance chains into account)
        """
        if expected_type == Identifier('object'):
            return True

        return resolved.type == expected_type
