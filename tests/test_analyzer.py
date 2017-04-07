import pytest

from thinglang import run
from thinglang.execution.errors import ReturnInConstructorError, EmptyMethodBody, EmptyThingDefinition, \
    ArgumentCountMismatch, UnresolvedReference
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.errors import ParseErrors
from thinglang.parser.symbols.functions import Access


def test_return_in_constructor():
    with pytest.raises(ReturnInConstructorError):
        run("""
thing Program
    setup
        return 10
    """)


def test_empty_method_body():
    with pytest.raises(ParseErrors) as error:
        run("""
thing Program
    setup
    does start
    """)

    assert error.value.args == (
        EmptyMethodBody(),
        EmptyMethodBody()
    )


def test_empty_thing_definition():
    with pytest.raises(EmptyThingDefinition):
        run("""
thing Program
    """)



def test_undefined_variable_exceptions():
    with pytest.raises(ParseErrors) as error:
        run("""
thing Program
    setup
        text out1 = "value of ou1"
        Output.write(out1, out2, out3)

        if some_condition
            text in1 = "value of in1"
            Output.write(out1, in1, out3)
        otherwise if operand1 + operand2 < operand3
            Output.write(out1, in1)

        repeat while out1 > in1
            Output.write(out1, in1, in2)

        Output.write(out1, out2, in1)

    does real_thing
        Output.write("at Program:real_thing")


thing ExternalClass
    does real_thing
        Output.write("at real_thing")
    """)

    assert error.value.args == (
        UnresolvedReference(LexicalIdentifier("out2")),  # Outer statement
        UnresolvedReference(LexicalIdentifier("out3")),

        UnresolvedReference(LexicalIdentifier("some_condition")),  # Conditional block

        UnresolvedReference(LexicalIdentifier("out3")),  # Inner statement

        UnresolvedReference(LexicalIdentifier("operand1")),  # Second conditional
        UnresolvedReference(LexicalIdentifier("operand2")),
        UnresolvedReference(LexicalIdentifier("operand3")),

        UnresolvedReference(LexicalIdentifier("in1")),  # Inner statement

        UnresolvedReference(LexicalIdentifier("in1")),  # Loop

        UnresolvedReference(LexicalIdentifier("in1")),  # Inner statement
        UnresolvedReference(LexicalIdentifier("in2")),

        UnresolvedReference(LexicalIdentifier("out2")),  # Outer statement
        UnresolvedReference(LexicalIdentifier("in1")),

    )


def test_method_call_reference_resolution():
    with pytest.raises(ParseErrors) as error:
        run("""
thing Program
    setup
        do_something()

        self.real_thing()
        self.missing_thing()

        ExternalClass.real_thing()
        ExternalClass.missing_thing()

    does real_thing
        Output.write("at Program:real_thing")


thing ExternalClass
    does real_thing
        Output.write("at real_thing")
    """)

    assert error.value.args == (
        UnresolvedReference(LexicalIdentifier("do_something")),
        UnresolvedReference(Access([LexicalIdentifier.self(), LexicalIdentifier("missing_thing")])),
        UnresolvedReference(Access([LexicalIdentifier("ExternalClass"), LexicalIdentifier("missing_thing")]))

    )


@pytest.mark.parametrize('line', ['', '1', '1, 2, 3'])
def test_argument_count_mismatch(line):
    with pytest.raises(ArgumentCountMismatch):
        run(f"""
thing Program
    setup
        self.add({line})

    does add with a, b
        return a + b

thing Person

    """)