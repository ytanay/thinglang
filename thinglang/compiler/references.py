class Reference(object):
    """
    The basic reference type
    """

    def __init__(self, type):
        super().__init__()
        self._type = type
        
    @property
    def type(self):
        """
        Returns the name of the type of the entity being referenced
        """
        return self._type


class ElementReference(Reference):
    """
    Describes a reference to an element, that is, a pair of references.

    Examples:
        - Member of an object instance
        - Method of a type
    """
    def __init__(self, thing, element, local=None):
        super(ElementReference, self).__init__(element.type)
        self.thing, self.element, self.local = thing, element, local

    @property
    def thing_index(self) -> int:
        """
        Returns the index of the thing being referenced
        """
        return self.thing.index

    @property
    def element_index(self) -> int:
        """
        Returns the relative index of the element being referenced
        """
        return self.element.index

    @property
    def local_index(self) -> int:
        """
        Returns the relative index of the local entity being referenced, if such a local entity exists
        """
        return self.local.index

    @property
    def is_local(self) -> bool:
        """
        Returns whether this reference also refers to a local element.
        """
        return self.local is not None

    @property
    def convention(self):
        """
        Returns the calling convention of this element, if it is a method call
        :return:
        """
        return self.element.convention

    @property
    def static(self) -> bool:
        """
        Returns whether the element is static
        """
        return self.element.static

    @property
    def kind(self) -> object:
        return self.element.kind


class LocalReference(Reference):
    """
    Describes a reference to a local entity on a method's stack frame
    """
    def __init__(self, local):
        super(LocalReference, self).__init__(local.type)
        self.local = local

    @property
    def local_index(self) -> int:
        """
        Returns the index of the local element
        """
        return self.local.index




