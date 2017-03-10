import traceback
from collections import namedtuple

from thinglang.common import ImmediateValue, ResolvableValue
from thinglang.execution.vm import ITOutput
from thinglang.parser.tokens import MethodCall, ReturnStatement, BaseToken, AssignmentOperation
import collections

class StackFrameTerminator(object):
    def __init__(self, target_arg=None):
        self.target_arg = target_arg

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
        targets = start.children[:]  # clone the list of children

        while targets:
            stack = self.stack[-1]
            target = targets.pop(0)
            terminator = StackFrameTerminator()

            self.set_context(target)

            if isinstance(target, StackFrameTerminator):  # Signifies the end of a function call
                last_frame = self.stack.pop()
                stack = self.stack[-1]
                self.log('Stack frame termination, with return value {}, binding to {}'.format(last_frame.return_value, target.target_arg))
                if target.target_arg is not None:
                    stack[target.target_arg] = last_frame.return_value
                continue

            if isinstance(target, ReturnStatement):
                if isinstance(target.value, ResolvableValue):
                    value = stack[target.value.value]
                else:
                    value = target.value.value
                terminator = next((i for i, x in enumerate(targets) if isinstance(x, StackFrameTerminator)))
                self.log('Assigning return value {} on stack - cleaning execution targets up to terminator at {}'.format(value, terminator))
                targets[0:terminator] = []
                self.stack[-1].return_value = value
                continue

            if isinstance(target, AssignmentOperation):
                if target.method is target.DECELERATION:
                    assert target.name.value not in stack, 'variable {} declaration but was found in stack'.format(
                        target.name.value)
                else:
                    assert target.name.value in stack, 'variable {} reassignment but is not in stack {}'.format(
                        target.name.value, target.context)

                if isinstance(target.value, MethodCall):
                    self.log('Assignment operation leading to method call, overriding terminator')
                    terminator = StackFrameTerminator(target.name.value)
                    target = target.value
                else:
                    stack[target.name.value] = target.value.evaluate(stack)

            if isinstance(target, MethodCall):
                context = self.resolve(self.stack[-1], target.target.value)
                args = target.arguments.evaluate(self.stack[-1])

                self.log('Method resolution: func={}, args={}'.format(context, args))

                if isinstance(context, collections.Callable):
                    context(args)
                else:
                    self.log('Generating stack frame, copying {} target children to target list: {}'.format(len(context.children), context.children))
                    self.create_stack_frame(ThingInstance(context.parent))

                    for name, value in zip(context.arguments, args):
                        self.stack[-1][name.value] = value
                    targets = context.children + [STACK_FRAME_TERMINATOR] + targets
            else:
                target.execute(self.stack[-1])

            if target.children:
                targets = target.children + targets

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
        print('Target: {}'.format(target.context if isinstance(target, BaseToken) else target))
        self.current_target = target

    def log(self, param):
        print('\t{}'.format(param))


class ThingInstance(object):

    def __init__(self, cls):
        self.cls = cls
        self.methods = {
            x.value: x for x in self.cls.children
        }
        self.members = {}

    def __contains__(self, item):
        return item in self.members or item in self.methods

    def __getitem__(self, item):
        return self.members.get(item) or self.methods.get(item)


class StackFrame(object):

    def __init__(self, instance):
        self.instance = instance
        self.data = {}
        self.idx = 0
        self.return_value = None

    def __setitem__(self, key, value):
        print('\tSET<{}> {}: {}'.format(self.idx, key, value))
        self.data[key] = (self.idx, value)

    def __getitem__(self, item):
        print('\tGET<{}> {}: {}'.format(self.idx, item, self.data[item][1]))
        return self.data[item][1]

    def __contains__(self, item):
        return item in self.data

    def enter(self):
        print('\tINCR<{}> -> <{}>'.format(self.idx, self.idx + 1))
        self.idx += 1

    def exit(self):
        print('\tDECR<{}> -> <{}>'.format(self.idx, self.idx - 1))
        self.data = {
            key: value for key, value in self.data.items() if value[1] != self.idx
        }

        self.idx -= 1


