class Describable(object):

    def __str__(self):
        return '{}({})'.format(type(self).__name__, self.describe())

    def __repr__(self):
        return self.__str__()

    def describe(self):
        return self.__dict__ if self.__dict__ else ''


class ValueType(object):
    pass


class ImmediateValue(ValueType):
    pass


class ResolvableValue(ValueType):
    pass


class ObtainableValue(ValueType):
    pass

