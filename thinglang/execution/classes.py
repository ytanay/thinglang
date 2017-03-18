class ThingInstance(object):

    def __init__(self, cls):
        self.cls = cls
        self.methods = {
            x.name: x for x in self.cls.children
        }
        self.members = {}

    def __contains__(self, item):
        return item in self.members or item in self.methods

    def __getitem__(self, item):
        return self.members.get(item) or self.methods.get(item)