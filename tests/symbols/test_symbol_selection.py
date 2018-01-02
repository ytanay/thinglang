import pytest

from tests.symbols import get_symbols
from thinglang.compiler.errors import NoMatchingOverload
from thinglang.compiler.references import Reference
from thinglang.lexer.values.identifier import Identifier
from thinglang.parser.values.named_access import NamedAccess
from thinglang.symbols.argument_selector import ArgumentSelector

SOURCE_OVERLOADING = '''

thing Container

thing Container1 extends Container
thing Container2 extends Container
    as Container1
thing Container3 extends Container
    as Container1
thing Container4 extends Container
    as Container1
    as Container2
    
thing Container1Child extends Container1
thing Container1Child2 extends Container1
    as Container2
thing Container2Child extends Container2
    

thing A
    does overloaded with Container1 container
    does overloaded with Container2 container
    does overloaded with Container2Child container
    does overloaded with Container1 c1, Container2 c2
    does overloaded with Container1 c1, Container2Child c2

'''


# TODO: verify no cast to base type!


SYMBOLS = get_symbols(SOURCE_OVERLOADING)
BASE = SYMBOLS.resolve(NamedAccess.auto('A.overloaded'))


def get_selection(*target_types):
    selector = BASE.element.selector(SYMBOLS)

    for target_type in target_types:
        selector.constraint(Reference(Identifier(target_type)))

    return selector.disambiguate(None)


def verify_selection(target_type, expected_index, expected_match):
    target = get_selection(*target_type)

    assert target.symbol.index == expected_index
    assert target.match == expected_match


def test_exact_match():
    verify_selection(['Container1'], 1, ArgumentSelector.EXACT)
    verify_selection(['Container2'], 2, ArgumentSelector.EXACT)  # Matches exactly, despite being castable
    verify_selection(['Container2Child'], 3, ArgumentSelector.EXACT)  # Matches exactly, despite being in an inheritance chain

    verify_selection(['Container1', 'Container2'], 4, ArgumentSelector.EXACT)
    verify_selection(['Container1', 'Container2Child'], 5, ArgumentSelector.EXACT)


def test_inheritance_match():
    verify_selection(['Container1Child'], 1, ArgumentSelector.INHERITANCE)
    verify_selection(['Container1Child2'], 1, ArgumentSelector.INHERITANCE)  # Matches in an inheritance chain, despite being castable


def test_casted_match():
    verify_selection(['Container3'], 1, ArgumentSelector.CAST)


def test_inheritance_directionality():  # Verify that a prent is not accepted in place of a child
    with pytest.raises(NoMatchingOverload) as exc:
        get_selection('Container')

    assert not exc.value.exact_matches and not exc.value.inheritance_matches and not exc.value.cast_matches


def test_cast_ambiguity():  # Verify cast ambiguity
    with pytest.raises(NoMatchingOverload) as exc:
        get_selection('Container4')

    assert not exc.value.exact_matches and not exc.value.inheritance_matches and len(exc.value.cast_matches) == 2

