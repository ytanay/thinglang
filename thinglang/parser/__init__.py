from typing import List

from thinglang.parser.nodes import RootNode
from thinglang.lexer.tokens import LexicalToken, LexicalGroupEnd

from thinglang.parser.vector import TokenVector, ParenthesesVector


def parse(lexical_groups) -> RootNode:
    """
    The parser takes a list<list<lexical-token>>, where each inner list (list<lexical-token>) is referred to as a lexical group (why? because).
    Each lexical group is parsed independently, through a process that reduces the group iteratively until no further reductions can be made.
    Then, lexical groups are processed in order, creating a tree structure based on indentation.
    Each TokenNode in the tree contains n-children, where each child is also a token node.
    The root node of this tree is returned
    """
    stack = [RootNode()]

    processed_groups = [collect_vectors(group).parse() for group in lexical_groups]

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

    for token in tokens:
        if token.VECTOR_START:
            stack.append(ParenthesesVector())
        elif token.VECTOR_END:
            if len(stack) <= 1:
                raise ValueError('No group to close')
            last = stack.pop()
            stack[-1].append(last)
        elif not isinstance(token, LexicalGroupEnd):  # TODO: remove group end token
            stack[-1].append(token)

    if len(stack) != 1:
        raise ValueError('Not all token vectors were closed - currently at depth {}'.format(len(stack)))

    return stack[0]
