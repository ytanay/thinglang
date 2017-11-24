import re


def camelcase_to_underscore(name):
    """
    Converts a camelCaseName to a underscore_separated_name
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def print_header(header, *params):
    """
    Prints a formatted header
    """
    print('{:#^80}'.format(' {} '.format(header)))

    if params:
        print(*params)
