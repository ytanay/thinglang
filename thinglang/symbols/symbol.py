class Symbol(object):

    METHOD, MEMBER = object(), object()
    PUBLIC = object()

    def __init__(self, name, kind, type, static, arguments=None):
        super(Symbol, self).__init__()

        self.index = None
        self.name, self.kind, self.type, self.static, self.arguments = name, kind, type, static, arguments
        self.visibility = Symbol.PUBLIC

    def update_index(self, new_index):
        self.index = new_index
        return self

    @classmethod
    def method(cls, name, return_type, static, arguments):
        return cls(name, cls.METHOD, return_type, static, [x.type for x in arguments])

    @classmethod
    def member(cls, name, type):
        return cls(name, cls.MEMBER, type, False)
