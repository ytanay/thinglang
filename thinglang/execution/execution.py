import collections
import traceback
from collections import namedtuple

from thinglang.common import ResolvableValue
from thinglang.execution.builtins import ITOutput
from thinglang.execution.classes import ThingInstance
from thinglang.execution.stack import StackFrameTerminator, StackFrame
from thinglang.parser.tokens import BaseToken
from thinglang.parser.tokens.base import AssignmentOperation
from thinglang.parser.tokens.functions import MethodCall, ReturnStatement
from thinglang.parser.tokens.logic import Conditional

STACK_FRAME_TERMINATOR = StackFrameTerminator()
ExecutionOutput = namedtuple('ExecutionOutput', ['output'])


class ExecutionEngine(object):
    def __init__(self, root):
        self.root = root
        self.stack = []
        self.heap = {
            x.value: x for x in root.children
        }

        self.heap['Output'] = ITOutput()

    def results(self):
        return ExecutionOutput(output=self.heap['Output'].data.strip())

    def __enter__(self):
        print('ExecutionEngine: starting')
        print('Parsed tree: {}'.format(self.root.tree()))
        assert self.root.get('Program') and self.root.get('Program').get('start'), 'Program must have an entry point'
        self.print_header('Program execution start')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.print_header('Execution end')
        print('ExecutionEngine: ended')
        if exc_val:
            print(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        self.print_header('Output')
        print(self.heap['Output'].data.strip())

    def execute(self):
        self.create_stack_frame(ThingInstance(self.root.get('Program')))

        start = self.root.get('Program').get('start')
        tokens = start.children[:]  # clone the list of children

        while tokens:
            stack = self.stack[-1]
            token = tokens.pop(0)
            terminator = StackFrameTerminator()

            self.set_context(token)

            if isinstance(token, StackFrameTerminator):  # Signifies the end of a function call
                last_frame = self.stack.pop()
                stack = self.stack[-1]
                self.log('Stack frame termination, with return value {}, binding to {}'.format(last_frame.return_value, token.target_arg))
                if token.target_arg is not None:
                    stack[token.target_arg] = last_frame.return_value
                continue

            if isinstance(token, ReturnStatement):
                if isinstance(token.value, ResolvableValue):
                    value = stack[token.value.value]
                else:
                    value = token.value.value
                terminator = next((i for i, x in enumerate(tokens) if isinstance(x, StackFrameTerminator)))
                self.log('Assigning return value {} on stack - cleaning execution targets up to terminator at {}'.format(value, terminator))
                tokens[0:terminator] = []
                self.stack[-1].return_value = value
                continue

            if isinstance(token, AssignmentOperation):
                if token.method is token.DECELERATION:
                    assert token.name.value not in stack, 'variable {} declaration but was found in stack'.format(
                        token.name.value)
                else:
                    assert token.name.value in stack, 'variable {} reassignment but is not in stack {}'.format(
                        token.name.value, token.context)

                if isinstance(token.value, MethodCall):
                    self.log('Assignment operation leading to method call, overriding terminator')
                    terminator = StackFrameTerminator(token.name.value)
                    token = token.value
                else:
                    stack[token.name.value] = token.value.evaluate(stack)

            if isinstance(token, MethodCall):
                context = self.resolve(self.stack[-1], token.target.target)
                args = token.arguments.evaluate(self.stack[-1])

                self.log('Method resolution: func={}, args={}'.format(context, args))

                if isinstance(context, collections.Callable):
                    self.log('Built in method, calling directly')
                    context(args)
                else:
                    self.log('Applying arguments {} -> {} -> {}'.format(context.arguments, token.arguments, args))
                    self.log('Generating stack frame, copying {} target children to target list: {}'.format(len(context.children), context.children))

                    self.create_stack_frame(ThingInstance(context.parent))
                    assert len(context.arguments) == len(args), 'Method expected {} arguments but recieved {}'.format(len(context.arguments), len(args))
                    for name, value in zip(context.arguments, args):
                        self.stack[-1][name.value] = value

                    tokens = context.children + [terminator] + tokens
                continue

            if isinstance(token, Conditional):
                if token.evaluate(stack):
                    tokens = token.children + tokens

            if token.ADVANCE:
                tokens = token.children + tokens

    def print_header(self, str):
        print('{:#^80}'.format(' {} '.format(str)))

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

    def log(self, param):
        print('\t{}'.format(param))

    def log_stack(self):
        if not self.stack[-1].data:
            return
        print('\tSTACK:')
        for key, value in self.stack[-1]:
            print('\t\t{} -> {}'.format(key, value))
