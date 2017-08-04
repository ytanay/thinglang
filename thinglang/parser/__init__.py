from typing import List

from thinglang.parser.nodes import RootNode
from thinglang.lexer.tokens import LexicalToken, LexicalGroupEnd

from thinglang.parser.vector import TokenVector, ParenthesesVector, VECTOR_CREATION_TOKENS


def parse(lexical_groups) -> RootNode:
    """
    The parser takes a list<list<lexical-token>>, where each inner list (list<lexical-token>) is referred to as a lexical group (why? because).
    Each lexical group is parsed independently, through a process that reduces the group iteratively until no further reductions can be made.
    Then, lexical groups are processed in order, creating a tree structure based on indentation.
    Each TokenNode in the tree contains n-children, where each child is also a token node.
    The root node of this tree is returned
    """
    stack = [RootNode()]
    processed_groups = []

    for group in lexical_groups:
        token_vector = collect_vectors(group)
        if not token_vector.empty():
            processed_groups.append(token_vector.parse())

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
            stack = stack[:next_indent - current_indent]

    return stack[0]


def collect_vectors(tokens: List[LexicalToken]) -> TokenVector:
    stack = [TokenVector()]
    closing_token = None

    for token in tokens:

        if type(token) in VECTOR_CREATION_TOKENS:
            closing_token, vector_cls = VECTOR_CREATION_TOKENS[type(token)]
            stack.append(vector_cls())
        elif closing_token and isinstance(token, closing_token):
            if len(stack) <= 1:
                raise ValueError('No group to close')
            last = stack.pop()
            stack[-1].append(last)
            if isinstance(closing_token, tuple):
                stack[-1].append(token)
            closing_token = None
        elif not isinstance(token, LexicalGroupEnd):  # TODO: remove group end token
            stack[-1].append(token)

    if len(stack) != 1:
        raise ValueError('Not all token vectors were closed - currently at depth {}'.format(len(stack)))

    return stack[0]
