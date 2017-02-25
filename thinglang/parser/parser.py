from thinglang.common import ValueType
from thinglang.lexer.lexical_tokens import LexicalDeclarationThing, LexicalIdentifier, LexicalDeclarationMethod, \
    LexicalQuote, LexicalParenthesesOpen, LexicalAccess, LexicalSeparator, LexicalParenthesesClose, \
    LexicalDunary, LexicalIndent, LexicalAssignment, SecondOrderLexicalDunary, FirstOrderLexicalDunary
from thinglang.parser.tokens import ThingDefinition, MethodDefinition, Access, String, ArgumentListPartial, MethodCall, \
    ArgumentList, ArithmeticOperation, RootToken, AssignmentOperation

PATTERNS = [
    ((LexicalDeclarationThing, LexicalIdentifier), ThingDefinition),  # thing Program
    ((LexicalDeclarationMethod, LexicalIdentifier), MethodDefinition),  # does start
    ((LexicalIdentifier, LexicalAccess, LexicalIdentifier), Access),  # person.name
    ((Access, ArgumentList), MethodCall),  # person.walk(...)
    ((ValueType, SecondOrderLexicalDunary, ValueType), ArithmeticOperation),  # 4 * 2
    ((ValueType, FirstOrderLexicalDunary, ValueType), ArithmeticOperation),  # 4 + 2
    ((LexicalParenthesesOpen, ValueType), ArgumentListPartial),  # (2
    ((ArgumentListPartial, LexicalSeparator, ValueType), ArgumentListPartial),  # (2, 3
    ((LexicalParenthesesOpen, LexicalParenthesesClose), ArgumentList),  # ()
    ((ArgumentListPartial, LexicalParenthesesClose), ArgumentList),  # (2, 3)
    ((LexicalIdentifier, LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation),  # number n = 1
    ((LexicalIdentifier, LexicalAssignment, ValueType), AssignmentOperation)  # n = 2

]


def parse(lexical_groups):
    """
    The parser takes a list<list<lexical-token>>, where each inner list (list<lexical-token>) is referred to as a lexical group (why? because).
    Each lexical group is parsed independently, through a process that reduces the group iteratively until no further reductions can be made.
    Then, lexical groups are processed in order, creating a tree structure based on indentation.
    Each TokenNode in the tree contains n-children, where each child is also a token node.
    The root node of this tree is returned
    """
    stack = [RootToken(None)]
    processed_groups = [x for x in [parse_group(group) for group in lexical_groups] if x]

    for idx, node in enumerate(processed_groups):

        parent = stack[-1]

        parent.attach(node)

        if idx + 1 >= len(processed_groups):
            continue

        next_indent = processed_groups[idx + 1].indent
        current_indent = node.indent
        if next_indent > current_indent:
            stack.append(node)

        if next_indent < current_indent:
            stack.pop()

    return stack[0]


def parse_group(group):
    """
    The lexical group parser continuously calls replace_in_place until no further replacements (i.e. reductions) can be made.
    The result of this iterative replacements must be a single token, otherwise a generic syntax error is said to have occured.
    For example, the source `Output.write("hello world")` would be emitted by the lexical analyzer as:
        LEXICAL_IDENTIFIER LEXICAL_ACCESS LEXICAL_IDENTIFIER LEXICAL_PARENTHESES_OPEN STRING_VALUE LEXICAL_PARENTHESES_CLOSE
    The parser would make the following replacements, in order:
        Access(id-1, id-2) LEXICAL_PARENTHESES_OPEN STRING_VALUE LEXICAL_PARENTHESES_CLOSE
        Access(id-1, id-2) ArgumentListPartial([string value]) LEXICAL_PARENTHESES_CLOSE
        Access(id-1, id-2) ArgumentList([string value])
        MethodCall(id-1, id-2, [string value])
    Therefore, the MethodCall token would be returned for this group.

    Additionally, the parser converts LEXICAL_INDENTATION tokens to actual indentation value which it stores directly on finalized token.
    :param group:
    :return:
    """
    while replace_in_place(group):
        pass

    process_indentation(group)

    if not group:
        return

    assert len(group) == 1, 'more than 1 element, {}'.format(group)
    return group[0]


def replace_in_place(group):
    """
    Given a list of lexical tokens, attempt to find partial matches, in order, using the replacements list defined above.
    Whenever a match succeeds, the matching slice is spliced out of place, and replaced with a parsed token instance which performs basic logical on the slice.
    The list is modified in place.
    :return: True if a replacement occurred, False otherwise
    """
    for pattern, target in PATTERNS:
        size = len(pattern)
        match_starts = filter_indices_by_type(group, pattern[0])

        for match_start in match_starts:
            slice = group[match_start:match_start + size]

            if match_pattern(pattern, slice):
                group[match_start:match_start + size] = [target(slice)]
                return True


def filter_indices_by_type(group, expected_class):
    """
    Returns the index of every element in a given list that is an instance of expected_class
    """
    return [idx for idx, entity in enumerate(group) if isinstance(entity, expected_class)]


def match_pattern(pattern, group):
    """
    Checks if a list matches a pattern exactly.
    """
    if len(pattern) != len(group):
        return False

    for type, instance in zip(pattern, group):
        if not isinstance(instance, type):
            return False

    return True


def process_indentation(group):
    """
    Converts a list of LEXICAL_INDENTATION tokens at the beginning of a parsed group into indentation value stored on the first real token.
    :param group:
    :return:
    """
    size = 0
    iterable = iter(group)

    if not group or not isinstance(group[0], LexicalIndent):
        return

    while isinstance(next(iterable), LexicalIndent):
        size += 1

    group[0:size] = []
    group[0].indent = size
