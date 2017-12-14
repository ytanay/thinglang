from thinglang.parser.common.list_type import ListInitialization


class ArgumentList(ListInitialization):
    """
    An argument list used for a MethodCall or MethodDefinition
    """

    def __repr__(self):
        return '{}'.format(', '.join(str(x) for x in self.arguments))