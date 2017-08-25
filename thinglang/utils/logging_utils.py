def print_header(header, *params):
    print('{:#^80}'.format(' {} '.format(header)))

    if params:
        print(*params)
