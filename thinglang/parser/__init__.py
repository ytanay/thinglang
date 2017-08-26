from typing import List

from thinglang.parser.nodes import RootNode
from thinglang.lexer.tokens import LexicalToken, LexicalGroupEnd

from thinglang.parser.vector import TokenVector, ParenthesesVector, VECTOR_CREATION_TOKENS


def parse(lexical_groups: List[List[LexicalToken]]) -> RootNode:
    """
    The parser takes a list<list<lexical-token>>, where each inner list (list<lexical-token>) is referred to as a lexical group.

    Each lexical group is parsed independently as follows:
        1. A nested TokenVector is created for the group
        2. The token vector is processed - that is to say, the lexical group is parsed using the thinglang parsing rules.
        3. The result of this parsing operation is an AST node, which includes indentation structure information.
        4. The AST node is added into a list of nodes pending attachment.

    Next, the nodes are processed in order, creating a tree structure based on indentation.
    The root node of this tree is returned.
    """
    stack = [RootNode()]
    processed_groups = []

    for group in lexical_groups:
        token_vector = collect_vectors(group)
        if not token_vector.empty:
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
    """
    Generates a token vector from a list of lexical tokens, using an iterative process where vector initiating and
    termination tokens (e.g. parentheses of all kinds) are resolved.
    """
    stack = [TokenVector()]
    closing_tokens = []

    for token in tokens:

        if type(token) in VECTOR_CREATION_TOKENS:
            closing_token, vector_cls = VECTOR_CREATION_TOKENS[type(token)]
            stack.append(vector_cls())
            closing_tokens.append(closing_token)
        elif closing_tokens and isinstance(token, closing_tokens[-1]):
            last = stack.pop()
            stack[-1].append(last)
            if isinstance(closing_tokens[-1], tuple):
                stack[-1].append(token)
            closing_tokens.pop()
        elif token.MUST_CLOSE:
            raise ValueError('Unexpected group end token')

        elif not isinstance(token, LexicalGroupEnd):  # TODO: remove group end token
            stack[-1].append(token)

    if len(stack) != 1:
        raise ValueError('Not all token vectors were closed - currently at depth {}'.format(len(stack)))

    return stack[0]
