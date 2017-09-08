from typing import List

from thinglang.utils import collection_utils
from thinglang.utils.source_context import SourceContext, SourceLine

from thinglang.lexer.lexical_definitions import OPERATORS, KEYWORDS, IDENTIFIER_STANDALONE
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue
from thinglang.lexer.tokens import LexicalGroupEnd, LexicalToken
from thinglang.lexer.tokens.base import LexicalInlineComment, LexicalIdentifier, LexicalQuote, LexicalTick
from thinglang.parser.nodes.base import InlineString, InlineCode


@collection_utils.drain()
def lexer(source: SourceContext) -> List[List[LexicalToken]]:
    for line in source:
        if not line.empty:
            yield analyze_line(line)


@collection_utils.drain(lambda x: x is not None)
def analyze_line(line: SourceLine):
    group, entity_class, current_ref, operator_working_set = '', None, None, OPERATORS

    for char, ref in line:

        if char not in operator_working_set:
            group += char  # continue appending characters to the current group

        else:  # i.e. if we are on an operator

            if group or (entity_class and entity_class.ALLOW_EMPTY):  # emit the collected group thus far
                yield finalize_group(group, char, entity_class)  # char is the character that terminated the group

            group = ""  # reset the group
            entity_class = operator_working_set[char]

            if entity_class is None:  # if there is no lexical entity for this character, nothing further to do
                continue

            # Some operators (e.g. ") cause the working operator set to change
            operator_working_set = entity_class.next_operator_set(operator_working_set, OPERATORS)

            # Stop iterating if we get to an inline lexical comment
            if entity_class is LexicalInlineComment:
                break

            # Emit an instance of the entity class if it is emittable
            if entity_class.EMITTABLE:
                yield OPERATORS[char](char)

    if group:
        yield finalize_group(group, StopIteration, entity_class)

    yield LexicalGroupEnd(None)


def finalize_group(group, termination_reason, entity_class):

    if group in KEYWORDS:
        return KEYWORDS[group](group) if KEYWORDS[group].EMITTABLE else None

    if group.isdigit():
        return LexicalNumericalValue(group)

    if termination_reason == '"':
        if entity_class is not LexicalQuote:
            raise ValueError("Unexpected end of string")
        return InlineString(group)

    if termination_reason == '`':
        if entity_class is not LexicalTick:
            raise ValueError("Unexpected end of inline code")
        return InlineCode(group)

    if is_identifier(group):
        if entity_class in (LexicalQuote, LexicalTick):
            raise ValueError("String was not closed")
        return LexicalIdentifier(group)

    if group:
        raise ValueError('Lexer: cannot terminate group {}'.format(group))


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))
