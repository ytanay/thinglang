from pprint import pprint


def log(*params):
    print('\t{}'.format(*params))


def print_header(header, *params, pretty=False):
    print('{:#^80}'.format(' {} '.format(header)))
    if not params:
        return

    if pretty:
        pprint(*params)
    else:
        print(*params)
