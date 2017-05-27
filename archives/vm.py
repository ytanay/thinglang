frames = [(None, None)]
stack = []
bytecode = [
    # func 1 - calls add
    ('STACK_INIT', 0),
    ('PUSH_CONSTANT', 3),
    ('PUSH_CONSTANT', 2),
    ('CALL', 6),
    ('PRINT', None),
    ('RETURN', None),

    # func 2 - add
    ('STACK_INIT', 3),
    ('SET', 0),
    ('SET', 1),
    ('PUSH', 0),
    ('PUSH', 1),
    ('BIN_ADD', None),
    ('PRINT', None),
    ('SET', 2),
    ('PUSH', 2),
    ('PUSH_CONSTANT', 2),
    ('BIN_MUL', None),
    ('RETURN', None)

]

idx = 0
return_idx = -1

while idx < len(bytecode):
    if idx == -1:
        print('Program end')
        break

    if idx < 0:
        raise Exception('Invalid index {}'.format(idx))

    op, arg = bytecode[idx]
    method_stack = frames[-1][1]

    if op == 'PUSH_CONSTANT':
        stack.append(arg)
    elif op == 'SET':
        method_stack[arg] = stack.pop()
    elif op == 'PUSH':
        stack.append(method_stack[arg])
    elif op == 'BIN_ADD':
        stack.append(stack.pop() + stack.pop())
    elif op == 'BIN_MUL':
        stack.append(stack.pop() * stack.pop())
    elif op == 'RETURN':
        val = stack.pop()
        stack.append(val)
        idx = frames.pop()[0]
        continue
    elif op == 'CALL':
        assert bytecode[arg][0] == 'STACK_INIT'
        return_idx = idx + 1
        idx = arg
        continue

    elif op == 'STACK_INIT':
        frames.append((return_idx, [None] * arg))
    elif op == 'PRINT':
        print('Head of stack: {}'.format(stack[-1]))

    idx += 1
