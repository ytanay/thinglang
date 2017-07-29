class Reference(object):
    def __init__(self, thing, element):
        self.thing, self.element = thing, element

    @property
    def thing_index(self):
        return self.thing.index

    @property
    def element_index(self):
        return self.element.index

    @property
    def convention(self):
        return self.element.convention
