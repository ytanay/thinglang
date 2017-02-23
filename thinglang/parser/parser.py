from thinglang.common import ValueType
from thinglang.lexer.lexical_tokens import LexicalDeclarationThing, LexicalIdentifier, LexicalDeclarationMethod, \
    LexicalQuote, LexicalParenthesesOpen, LexicalAccess, LexicalSeparator, LexicalParenthesesClose, \
    LexicalDunary, LexicalIndent, LexicalAssignment, SecondOrderLexicalDunary, FirstOrderLexicalDunary
from thinglang.parser.tokens import ThingDefinition, MethodDefinition, Access, String, ArgumentListPartial, MethodCall, ArgumentList, ArithmeticOperation, RootToken, AssignmentOperation

PATTERNS = [
    ((LexicalDeclarationThing, LexicalIdentifier), ThingDefinition), # thing Program
    ((LexicalDeclarationMethod, LexicalIdentifier), MethodDefinition), # does start
    ((LexicalIdentifier, LexicalAccess, LexicalIdentifier), Access), # person.name
    ((Access, ArgumentList), MethodCall), # person.walk(...)
    ((ValueType, SecondOrderLexicalDunary, ValueType), ArithmeticOperation), # 4 * 2
    ((ValueType, FirstOrderLexicalDunary, ValueType), ArithmeticOperation), # 4 + 2
    ((LexicalParenthesesOpen, ValueType), ArgumentListPartial), # (2
    ((ArgumentListPartial, LexicalSeparator, ValueType), ArgumentListPartial), # (2, 3
    ((LexicalParenthesesOpen, LexicalParenthesesClose), ArgumentList), # ()
    ((ArgumentListPartial, LexicalParenthesesClose), ArgumentList), # (2, 3)
    ((LexicalIdentifier, LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation), # number n = 1
    ((LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation) # n = 2

]


def parse(lexical_groups):
    stack = [RootToken(None)]
    processed_groups = [x for x in [parse_group(group) for group in lexical_groups] if x]

    for idx, node in enumerate(processed_groups):

        parent = stack[-1]

        parent.attach(node)

        if idx + 1 >= len(processed_groups):
            continue

        next_indent = get_indent(processed_groups[idx + 1])
        current_indent = get_indent(node)
        if next_indent > current_indent:
            stack.append(node)

        if next_indent < current_indent:
            stack.pop()

    return stack[0]


def parse_group(group):
    while len(group) > 1:
        if not replace_in_place(group):
            break
    process_indentation(group)
    if not group:
        return
    assert len(group) == 1, 'more than 1 element, {}'.format(group)
    return group[0]


def replace_in_place(group):
    for pattern, target in PATTERNS:
        size = len(pattern)
        match_starts = first_matching(group, pattern[0])

        for match_start in match_starts:
            slice = group[match_start:match_start + size]
            if match_pattern(pattern, slice):
                group[match_start:match_start + size] = [target(slice)]
                return True


def first_matching(group, expected_class):
    return [idx for idx, entity in enumerate(group) if isinstance(entity, expected_class)]


def match_pattern(pattern, group):
    if len(pattern) != len(group):
        return False
    for type, instance in zip(pattern, group):
        if not isinstance(instance, type):
            return False
    return True


def process_indentation(group):
    size = 0
    iterable = iter(group)

    if not group or not isinstance(group[0], LexicalIndent):
        return

    while isinstance(next(iterable), LexicalIndent):
        size += 1

    group[0:size] = []
    group[0].indent = size


def get_indent(group):
    return group.indent


