import collections
import traceback
from collections import namedtuple

import itertools

from thinglang import utils
from thinglang.execution.builtins import ThingObjectInput, ThingObjectOutput
from thinglang.execution.classes import ThingInstance
from thinglang.execution.errors import RedeclaredVariable
from thinglang.execution.stack import StackFrameTerminator, StackFrame, StackScopeTerminator
from thinglang.execution.resolver import Resolver
from thinglang.lexer.symbols.base import LexicalIdentifier
from thinglang.parser.tokens import BaseToken
from thinglang.parser.tokens.base import AssignmentOperation
from thinglang.parser.tokens.functions import MethodCall, ReturnStatement
from thinglang.parser.tokens.logic import Conditional, ElseBranchInterface, Loop

ExecutionOutput = namedtuple('ExecutionOutput', ['output'])


class ExecutionEngine(object):
    def __init__(self, ast):
        self.ast = ast

        self.stack = Stack()

        self.heap = {  # Collect all root level ThingDefinitions
            x.name: x for x in ast.children
        }

        self.heap.update({  # Mix in builtins, with a reference to the heap object
            LexicalIdentifier(x.INTERNAL_NAME): x(self.heap) for x in BUILTINS
        })

        self.resolver = Resolver(self.stack, self.heap)

    def __enter__(self):
        assert self.ast.get('Program') and self.ast.get('Program').get(LexicalIdentifier.constructor()), 'Program must have an entry point'
        utils.print_header('Execution')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_val:
            utils.print_header('Execution summary (exceptions)')
            print(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        utils.print_header('Output')
        print('\n'.join(self.heap['Output'].data))

    def execute(self):
        self.create_stack_frame(ThingInstance(self.root.get('Program')))
        root_instance = ThingInstance(self.ast.get('Program'))

        start = self.root.get('Program').get('start')
        tokens = start.children[:]  # clone the list of children

        while tokens:
            stack = self.stack[-1]
            token = tokens.pop(0)
            terminator = None

            self.set_context(token)

            if isinstance(token, StackFrameTerminator):  # Signifies the end of a function call
                last_frame = self.stack.pop()
                stack = self.stack[-1]
                utils.log('Stack frame termination, with return value {}, binding to {}'.format(last_frame.return_value, token.target_arg))
                if token.target_arg is not None:
                    stack[token.target_arg] = last_frame.return_value
                continue

            if isinstance(token, StackScopeTerminator):
                stack.exit()
                continue

            if isinstance(token, ReturnStatement):
                if isinstance(token.value, LexicalIdentifier):
                    value = stack[token.value.value]
                else:
                    value = token.value.value
                terminator = next((i for i, x in enumerate(tokens) if isinstance(x, StackFrameTerminator)))
                utils.log('Assigning return value {} on stack - cleaning execution targets up to terminator at {}'.format(value, terminator))
                tokens[0:terminator] = []
                self.stack[-1].return_value = value
                continue

            if isinstance(token, AssignmentOperation):
                if token.method is token.DECELERATION and token.name.value in stack:
                    raise RedeclaredVariable('variable {} declaration but was found in stack'.format(
                        token.name.value))
                elif token.method is token.REASSIGNMENT and token.name.value not in stack:
                    raise RuntimeError('variable {} reassignment but is not in stack {}'.format(
                        token.name.value, token.context))

                if isinstance(token.value, MethodCall):
                    utils.log('Assignment operation leading to method call, overriding terminator')
                    terminator = StackFrameTerminator(token.name.value)
                    token = token.value
                else:
                    stack[token.name.value] = token.value.evaluate(stack)

            if isinstance(token, MethodCall):
                context = self.resolve(self.stack[-1], token.target.target)
                args = token.arguments.evaluate(self.stack[-1])

                utils.log('Method resolution: func={}, args={}'.format(context, args))

                if isinstance(context, collections.Callable):
                    utils.log('Built in method, calling directly')
                    result = context(*args)
                    if terminator is not None:
                        stack[terminator.target_arg] = result
                else:
                    utils.log('Applying arguments {} -> {} -> {}'.format(context.arguments, token.arguments, args))
                    utils.log('Generating stack frame, copying {} target children to target list: {}'.format(len(context.children), context.children))

                    self.create_stack_frame(ThingInstance(context.parent))
                    assert len(context.arguments) == len(args), 'Method expected {} arguments but recieved {}'.format(len(context.arguments), len(args))
                    for name, value in zip(context.arguments, args):
                        self.stack[-1][name.value] = value

                    tokens = context.children + [terminator or StackFrameTerminator()] + tokens
                continue

            if isinstance(token, Conditional):
                if token.evaluate(stack):
                    stack.enter()
                    tokens = token.children + \
                             [StackScopeTerminator()] + \
                             list(itertools.dropwhile(lambda x: isinstance(x, ElseBranchInterface), tokens)) # Remove all directly following else-like branches

            if isinstance(token, Loop):
                if token.evaluate(stack):
                    tokens = token.children + [token] + tokens

            if token.ADVANCE:
                tokens = token.children + tokens

    def results(self):
        return ExecutionOutput(output='\n'.join(self.heap['Output'].data))

    def create_stack_frame(self, instance):
        self.stack.append(StackFrame(instance))

    def resolve(self, stack, target):
        if target[0] == 'self':
            context = stack.instance
            target = target[1:]
        else:
            context = self.heap
        for component in target:
            if component not in context:
                raise ValueError('Cannot find {} in {}'.format(component, context))
            context = context[component]
        return context

    def set_context(self, target):
        print('Target: {} ({})'.format(target.context if isinstance(target, BaseToken) else target, target))
        self.log_stack()
        self.current_target = target

    def log_stack(self):
        if not self.stack[-1].data:
            return
        print('\tSTACK:')
        for key, value in self.stack[-1]:
            print('\t\t{} -> {}'.format(key, value))
