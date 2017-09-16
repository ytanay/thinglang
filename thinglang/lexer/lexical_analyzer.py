from typing import List

from thinglang.lexer.grouping.quote import LexicalQuote
from thinglang.lexer.grouping.backtick import LexicalBacktick
from thinglang.lexer.lexical_definitions import OPERATORS, KEYWORDS, IDENTIFIER_STANDALONE
from thinglang.lexer.tokens.inline_comment import LexicalInlineComment
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.tokens.misc import LexicalGroupEnd
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.values.inline_code import InlineCode
from thinglang.parser.values.inline_text import InlineString
from thinglang.utils import collection_utils
from thinglang.utils.source_context import SourceContext, SourceLine


@collection_utils.drain()
def lexer(source: SourceContext) -> List[List[LexicalToken]]:
    for line in source:
        if not line.empty:
            yield analyze_line(line)


@collection_utils.drain(lambda x: x is not None)
def analyze_line(line: SourceLine):
    group, entity_class, start_ref, operator_working_set = '', None, None, OPERATORS

    for char, current_ref in line:

        if start_ref is None:
            start_ref = current_ref  # update the group's starting source reference

        if char not in operator_working_set:
            group += char  # continue appending characters to the current group

        else:  # i.e. if we are on an operator

            if group or (entity_class and entity_class.ALLOW_EMPTY):  # emit the collected group thus far
                yield finalize_group(group, char, entity_class, current_ref - start_ref)

            group, start_ref = '', None  # reset the group and the starting source reference
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
                yield OPERATORS[char](char, current_ref)

    if group:
        yield finalize_group(group, StopIteration, entity_class, current_ref - start_ref + 1)

    yield LexicalGroupEnd()


def finalize_group(group, terminating_char, entity_class, source_ref):

    if group in KEYWORDS:
        return KEYWORDS[group](group, source_ref) if KEYWORDS[group].EMITTABLE else None

    if group.isdigit():
        return NumericValue(group, source_ref)

    if terminating_char == '"':
        if entity_class is not LexicalQuote:
            raise ValueError("Unexpected end of string")
        return InlineString(group, source_ref)

    if terminating_char == '`':
        if entity_class is not LexicalBacktick:
            raise ValueError("Unexpected end of inline code")
        return InlineCode(group, source_ref)

    if is_identifier(group):
        if entity_class in (LexicalQuote, LexicalBacktick):
            raise ValueError("String was not closed")
        return Identifier(group, source_ref)

    if group:
        raise ValueError('Lexer: cannot terminate group {}'.format(group))


def is_identifier(component):
    return bool(IDENTIFIER_STANDALONE.match(component))
