import collections
import copy

from thinglang.compiler.errors import NoMatchingOverload
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.definitions.cast_tag import CastTag

SymbolOption = collections.namedtuple('SymbolOption', ['symbol', 'remaining_arguments'])
SymbolTarget = collections.namedtuple('SymbolTarget', ['symbol', 'match'])


class ArgumentSelector(object):
    """
    Aids in disambiguating overloaded method symbols contained in MergedSymbol objects.
    Managed state regarding arguments already observed, and filters out overloads and all arguments are processed.
    If a matching overload exists, it is returned - otherwise, an exception is thrown.
    """

    EXACT, INHERITANCE, CAST = object(), object(), object()

    def __init__(self, symbols, context):
        self.symbols, self.context, self.collected_arguments = symbols, context, []

        self.all_options = self.map_options(symbols)
        self.exact_matches, self.inheritance_matches, self.casted_matches = (self.map_options(symbols) for _ in range(3))

    def constraint(self, resolved):
        """
        Filters out option groups that do not expect to see the resolved type as their next argument
        """
        self.collected_arguments.append(resolved)

        self.exact_matches = self.filter(self.exact_matches, self.exact_match, resolved)
        self.inheritance_matches = self.filter(self.inheritance_matches, self.inheritance_match, resolved)
        self.casted_matches = self.filter(self.casted_matches, self.casted_match, resolved)

    def filter(self, option_set, predicate, resolved):
        return [x for x in option_set if x.remaining_arguments and predicate(x.remaining_arguments.pop(0), resolved)]

    def disambiguate(self, source_ref):
        """
        Selects the best matching overload, if one exists
        """

        self.exact_matches = self.finalize(self.exact_matches)
        self.inheritance_matches = self.finalize(self.inheritance_matches)
        self.casted_matches = self.finalize(self.casted_matches)

        if self.select_single(self.exact_matches, source_ref):
            return SymbolTarget(self.exact_matches.pop().symbol, self.EXACT)

        if self.select_single(self.inheritance_matches, source_ref):
            return SymbolTarget(self.inheritance_matches.pop().symbol, self.INHERITANCE)

        if self.select_single(self.casted_matches, source_ref, last_resort=True):
            return SymbolTarget(self.casted_matches.pop().symbol, self.CAST)

    def select_single(self, option_group, source_ref, last_resort=False):
        if len(option_group) == 1:
            return True

        if option_group or last_resort:
            raise NoMatchingOverload(self.symbols, self.collected_arguments, self.exact_matches, self.inheritance_matches, self.casted_matches, source_ref)

    def exact_match(self, expected_type, resolved):
        # TODO: generic identifiers should not be exportable
        return expected_type == resolved.type

    def inheritance_match(self, expected_type, resolved):
        expected_type, resolved_type = self.normalize_type(expected_type), self.normalize_type(resolved.type)
        return any(parent_type.name == expected_type for parent_type in self.context.symbols.inheritance(resolved_type))

    def casted_match(self, expected_type, resolved):
        expected_type, resolved_type = self.normalize_type(expected_type), self.normalize_type(resolved.type)
        tag, symbol_map = CastTag(expected_type), self.context.symbols[resolved_type] # TODO: add warning when cast was not selected due to implicitness?
        return self.inheritance_match(expected_type, resolved) or (tag in symbol_map and symbol_map[tag].implicit)

    @staticmethod
    def map_options(symbols):
        return [SymbolOption(symbol, copy.deepcopy(symbol.arguments)) for symbol in symbols]

    @staticmethod
    def finalize(exact_matches):
        return [x for x in exact_matches if not x.remaining_arguments]

    def normalize_type(self, param):
        return param if param in self.context.symbols else self.context.resolve(param).type
