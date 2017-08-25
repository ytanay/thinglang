class Reference(object):

    def __init__(self, type):
        super().__init__()
        self._type = type
        
    @property
    def type(self):
        return self._type


class ElementReference(Reference):
    def __init__(self, thing, element, local=None):
        super(ElementReference, self).__init__(element.type)
        self.thing, self.element, self.local = thing, element, local

    @property
    def thing_index(self):
        return self.thing.index

    @property
    def element_index(self):
        return self.element.index

    @property
    def local_index(self):
        return self.local.index

    @property
    def is_local(self):
        return self.local is not None

    @property
    def convention(self):
        return self.element.convention

    @property
    def static(self):
        return self.element.static


class LocalReference(Reference):
    def __init__(self, local):
        super(LocalReference, self).__init__(local.type)
        self.local = local

    @property
    def local_index(self):
        return self.local.index


class StaticReference(Reference):
    def __init__(self, value):
        super(StaticReference, self).__init__(value.type)
        self.value = value



