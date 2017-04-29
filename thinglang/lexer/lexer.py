import re

from thinglang.utils.token_context import TokenContext
from thinglang.lexer.lexical_definitions import OPERATORS, KEYWORDS, is_identifier
from thinglang.lexer.tokens.arithmetic import LexicalNumericalValue
from thinglang.lexer.tokens import LexicalGroupEnd
from thinglang.lexer.tokens.base import LexicalInlineComment, LexicalIdentifier, LexicalQuote
from thinglang.parser.symbols.base import InlineString


def lexer(source):
    for idx, line in enumerate(source.strip().split('\n')):
        yield list(contextualize_lexical_output(analyze_line(line), line, idx))


def analyze_line(line):
    group = ""
    operator_working_set = OPERATORS
    entity_class = None

    for char in line:

        if char not in operator_working_set:
            group += char  # continue appending characters to the current group

        else:  # i.e. if we are on an operator

            if group or (entity_class and entity_class.ALLOW_EMPTY):  # emit the collected group thus far
                yield finalize_group(group, char)  # char is the character that terminated the group

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
        yield finalize_group(group, StopIteration)

    yield LexicalGroupEnd(None)


def finalize_group(group, termination_reason):
    if group in KEYWORDS:
        return KEYWORDS[group](group) if KEYWORDS[group].EMITTABLE else None

    if group.isdigit():
        return LexicalNumericalValue(group)

    if termination_reason == '"':
        return InlineString(group)

    if is_identifier(group):
        return LexicalIdentifier(group)

    if group:
        raise RuntimeError('Lexer: cannot finalize group {}'.format(group))


def contextualize_lexical_output(lexical_group, line, idx):
    for entity in lexical_group:
        if entity is not None:
            entity.context = TokenContext(line, idx)
            yield entity
