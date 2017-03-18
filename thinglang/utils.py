def flatten_list(l):
    return [item for sublist in l for item in sublist]


def log(*params):
    print('\t{}'.format(*params))


def print_header(header, *params):
    print('{:#^80}'.format(' {} '.format(header)))
    if params:
        print(*params)

