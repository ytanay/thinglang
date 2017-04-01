import collections
import traceback


from thinglang import utils
from thinglang.execution.builtins import BUILTINS
from thinglang.execution.classes import ThingInstance
from thinglang.execution.resolver import Resolver
from thinglang.execution.stack import StackFrameTerminator, Stack, StackScopeTerminator, Frame
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.parser.symbols import BaseSymbol
from thinglang.parser.symbols.base import AssignmentOperation
from thinglang.parser.symbols.functions import MethodCall, ReturnStatement
from thinglang.parser.symbols.logic import Conditional, ElseBranchInterface, Loop

ExecutionOutput = collections.namedtuple('ExecutionOutput', ['output'])


class ExecutionEngine(object):
    def __init__(self, ast):
        self.ast = ast
        self.stack = Stack()
        self.targets = collections.deque()
        self.current_target = None

        self.heap = {  # Collect all root level ThingDefinitions
            x.name: x for x in ast.children
        }

        self.heap.update({  # Mix in builtins, with a reference to the heap object
            LexicalIdentifier(x.INTERNAL_NAME): x(self.heap) for x in BUILTINS
        })

        self.resolver = Resolver(self.stack, self.heap)

    def __enter__(self):
        assert self.ast.get(LexicalIdentifier('Program')) and self.ast.get(LexicalIdentifier('Program')).get(LexicalIdentifier.constructor()), 'Program must have an entry point'
        utils.print_header('Execution')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            utils.print_header('Execution summary (exceptions)')
            print(''.join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        utils.print_header('Output')
        print('\n'.join(self.heap[LexicalIdentifier('Output')].data))

    def execute(self):
        root_instance = ThingInstance(self.ast.get(LexicalIdentifier('Program')))
        self.targets.extend(root_instance.methods[LexicalIdentifier.constructor()].children)

        self.stack.push(Frame(root_instance))  # Creates the root stack frame

        while self.targets:
            target = self.get_target()
            terminator = None

            if isinstance(target, Conditional):
                if target.evaluate(self.resolver):
                    self.stack.enter()
                    self.drop_while(ElseBranchInterface) # Remove all directly following else-like branches
                    self.add_targets(target.children, [StackScopeTerminator()])

                continue

            if isinstance(target, Loop):
                if target.evaluate(self.resolver):
                    self.add_targets(target.children, [target])
                continue

            if isinstance(target, StackFrameTerminator):  # Signifies the end of a function call
                last_frame = self.stack.pop()
                utils.log('Stack frame termination, with return value {}, binding to {}'.format(last_frame.return_value, target.target_arg))

                if target.constructor:
                    self.stack[target.target_arg] = last_frame.instance
                elif target.target_arg is not None:
                    self.stack[target.target_arg] = last_frame.return_value

                continue

            if isinstance(target, StackScopeTerminator):
                self.stack.exit()
                continue

            if isinstance(target, ReturnStatement):
                value = target.value.evaluate(self.resolver)

                self.drop_until(StackFrameTerminator)

                utils.log(
                    'Applying return value {} on stack - cleaning execution targets up to terminator at {}'.format(
                        value, terminator))

                self.stack.returns(value)
                continue

            if isinstance(target, AssignmentOperation):
                if isinstance(target.value, MethodCall):
                    utils.log(f'Assignment operation leading to method call, binding terminator to {target.name}')
                    terminator = StackFrameTerminator(target.name)
                    target = target.value
                else:
                    self.resolver.set(target.name, target.value.evaluate(self.resolver))

            if isinstance(target, MethodCall):
                context = self.resolver.resolve(target.target)
                args = target.arguments.evaluate(self.resolver)

                utils.log(f'Method resolution: func={context}, args={args}')

                if isinstance(context, collections.Callable):
                    utils.log('Built in method, calling directly')
                    result = context(*args)
                    if terminator is not None:
                        self.stack[terminator.target_arg] = result
                else:
                    utils.log(f'Applying arguments {context.arguments} -> {target.arguments} -> {args}')
                    utils.log(
                        f'Generating stack frame, copying {len(context.children)} target children to target list: {context.children}')

                    instance = ThingInstance(context.parent) if target.constructing_call else self.resolver.resolve(target.target[:-1])
                    self.stack.push(Frame(instance))
                    assert len(context.arguments) == len(args), 'Method expected {} arguments but recieved {}'.format(len(context.arguments), len(args))
                    for name, value in zip(context.arguments, args):
                        self.stack[name] = value

                    terminator = (terminator or StackFrameTerminator()).constructs(target.constructing_call)
                    self.add_targets(context.children, [terminator])

                continue

            if target.ADVANCE:
                self.add_targets(target.children)

    def results(self):
        return ExecutionOutput(output='\n'.join(self.heap[LexicalIdentifier('Output')].data))

    def log_stack(self):
        if self.stack.data:
            print('\tSTACK:')
            for key, value in self.stack.data.items():
                print('\t\t{} -> {}'.format(key, value))

        if self.stack.instance.members:
            print('\tMEMBERS:')
            for key, value in self.stack.instance.members.items():
                print('\t\t{} -> {}'.format(key, value))

    def get_target(self):
        target = self.targets.popleft()
        print(f'Target: {target.context if isinstance(target, BaseSymbol) else target} ({target})')
        self.log_stack()
        self.current_target = target
        return target

    def drop_until(self, cls):
        while self.targets and not isinstance(self.targets[0], cls):
            self.targets.popleft()

    def drop_while(self, cls):
        while self.targets and isinstance(self.targets[0], cls):
            self.targets.popleft()

    def add_targets(self, *args):
        for arg in reversed(args):
            self.targets.extendleft(reversed(arg))

