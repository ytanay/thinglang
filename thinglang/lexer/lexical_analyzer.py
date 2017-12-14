from typing import List

from thinglang.lexer.grouping.quote import LexicalQuote
from thinglang.lexer.grouping.backtick import LexicalBacktick
from thinglang.lexer.lexical_definitions import OPERATORS, KEYWORDS, IDENTIFIER_STANDALONE
from thinglang.lexer.tokens.inline_comment import LexicalInlineComment
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.tokens.misc import LexicalGroupEnd
from thinglang.lexer.values.identifier import Identifier
from thinglang.lexer.values.numeric import NumericValue
from thinglang.parser.values.inline_text import InlineString
from thinglang.utils import collection_utils
from thinglang.utils.source_context import SourceContext, SourceLine


@collection_utils.drain()
def lexer(source: SourceContext) -> List[List[LexicalToken]]:
    """
    Performs lexical analysis on every line of code in the source independently
    """
    for line in source:
        if not line.empty:
            yield analyze_line(line)


@collection_utils.drain(lambda x: x is not None)
def analyze_line(line: SourceLine) -> List[LexicalToken]:
    """
    Analyze a line of source code, emitting a list of lexical tokens
    """
    operator_working_set, buffer, entity_class, start_ref, current_ref = OPERATORS, '', None, None, None

    for char, current_ref in line:

        if start_ref is None:
            start_ref = current_ref  # update the group's starting source reference

        if char not in operator_working_set:
            buffer += char  # continue appending characters to the current group

        else:  # i.e. if we are on an operator

            if buffer or (entity_class and entity_class.ALLOW_EMPTY):  # emit the collected group thus far
                yield finalize_buffer(buffer, char, entity_class, current_ref - start_ref)

            buffer, start_ref = '', None  # reset the group and the starting source reference
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

    if buffer:
        yield finalize_buffer(buffer, StopIteration(), entity_class, current_ref - start_ref + 1)

    yield LexicalGroupEnd()


def finalize_buffer(buffer: str, terminating_char, entity_class, source_ref) -> LexicalToken:
    """
    Finalize a character buffer into a lexical token
    :param buffer: the characters collected thus far
    :param terminating_char: the character which caused the buffer termination (not included in buffer)
    :param entity_class: the current entity being collected (generally, a type of quote, or none)
    :param source_ref: a reference to the source from which these tokens were derived
    """
    if buffer in KEYWORDS:
        return KEYWORDS[buffer](buffer, source_ref) if KEYWORDS[buffer].EMITTABLE else None

    if buffer.isdigit():
        return NumericValue(buffer, source_ref)

    if terminating_char == '"':
        if entity_class is not LexicalQuote:
            raise ValueError("Unexpected end of string")
        return InlineString(buffer, source_ref)

    if terminating_char == '`':
        if entity_class is not LexicalBacktick:
            raise ValueError("Unexpected end of inline code")
        return InlineString(buffer, source_ref)

    if is_identifier(buffer):
        if entity_class in (LexicalQuote, LexicalBacktick):
            raise ValueError("String was not closed")
        return Identifier(buffer, source_ref)

    if buffer:
        raise ValueError('Lexer: cannot terminate group {}'.format(buffer))


def is_identifier(buffer) -> bool:
    """
    Checks if the collected buffer can be interpreted as an identifier
    """
    return bool(IDENTIFIER_STANDALONE.match(buffer))
