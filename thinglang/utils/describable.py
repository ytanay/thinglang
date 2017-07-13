import re


class Describable(object):

    def __str__(self):
        return '{}({})'.format(type(self).__name__, self.describe())

    def __repr__(self):
        return self.__str__()

    def describe(self):
        return self.__dict__ if self.__dict__ else ''

    def implements(self, cls):
        return isinstance(self, cls)

    @classmethod
    def construct(cls, slice):
        return cls(slice)


def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()