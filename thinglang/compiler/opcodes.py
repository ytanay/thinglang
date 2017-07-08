OPCODES = {name: idx for idx, name in enumerate([
    'INVALID',
    'NOP',

    'PUSH',  # pushes a reference into the stack
    'PUSH_STATIC',  # pushes static data into the stack
    'PUSH_NULL',

    'POP',  # pop anything to void

    'SET',  # pop a reference from the stack and assign it
    'SET_STATIC',  # set a reference to static data

    'CALL',
    'CALL_INTERNAL',
    'RETURN',

    'JUMP',
    'CONDITIONAL_JUMP',

    'PRINT',

    'METHOD_END'
])}

