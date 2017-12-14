from typing import List

from thinglang.lexer.definitions.tags import LexicalArgumentListIndicator, LexicalDeclarationReturnType
from thinglang.lexer.grouping.brackets import LexicalBracketOpen, LexicalBracketClose
from thinglang.lexer.grouping.parentheses import LexicalParenthesesOpen, LexicalParenthesesClose
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.operators.comparison import LexicalLessThan, LexicalGreaterThan
from thinglang.lexer.tokens.misc import LexicalGroupEnd
from thinglang.parser.nodes.root_node import RootNode
from thinglang.parser.vector import TokenVector, ParenthesesVector, BracketVector, TypeVector, ParameterVector

VECTOR_CREATION_TOKENS = {
    LexicalParenthesesOpen: (LexicalParenthesesClose, ParenthesesVector, True),
    LexicalBracketOpen: (LexicalBracketClose, BracketVector, True),
    LexicalArgumentListIndicator: ((LexicalDeclarationReturnType, LexicalGroupEnd), TypeVector, True),
    LexicalLessThan: (LexicalGreaterThan, ParameterVector, False)
}


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
            closing_token, vector_cls, strictly_vectorizing = VECTOR_CREATION_TOKENS[type(token)]
            if not strictly_vectorizing and not any(isinstance(token, closing_token) for token in tokens):
                # This is used to deal with angle brackets serving a dual purpose - comparison and parameter lists
                # Those tokens are not strictly vectorizing - we only assume they are if we can find a closing token
                # Additionally, the resulting vector can be demoted if it cannot be parsed as a ParameterVector
                stack[-1].append(token)
                continue

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

        elif not isinstance(token, LexicalGroupEnd):
            stack[-1].append(token)

    if len(stack) != 1:
        raise ValueError('Not all token vectors were closed - currently at depth {}'.format(len(stack)))

    return stack[0]

