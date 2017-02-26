from thinglang.common import Describeable, ValueType


# Base type
class LexicalEntity(Describeable):
    emittable = True

    def __init__(self, raw):
        self.raw = raw


# Derived types
class LexicalAccess(LexicalEntity): pass # a.b

class LexicalParenthesesOpen(LexicalEntity): pass # (
class LexicalParenthesesClose(LexicalEntity): pass # )

class LexicalQuote(LexicalEntity): # "
    emittable = False

class LexicalSeparator(LexicalEntity): pass # ,

class LexicalIndent(LexicalEntity): pass # <TAB>

class LexicalAssignment(LexicalEntity): pass

class LexicalDunary(LexicalEntity):
    def __init__(self, operator):
        super(LexicalDunary, self).__init__(operator)
        self.operator = operator


class FirstOrderLexicalDunary(LexicalDunary): pass
class SecondOrderLexicalDunary(LexicalDunary): pass


class LexicalIdentifier(LexicalEntity, ValueType):
    def __init__(self, value):
        super(LexicalIdentifier, self).__init__(value)
        self.value = value

    def describe(self):
        return self.value

    def evaluate(self, stack):
        return stack[self.value]

class LexicalNumericalValue(LexicalEntity, ValueType):
    def __init__(self, value):
        super(LexicalNumericalValue, self).__init__(value)
        self.value = int(value)

    def evaluate(self, stack):
        return self.value

class LexicalDeclarationThing(LexicalEntity): pass
class LexicalDeclarationMethod(LexicalEntity): pass
class LexicalArgumentListIndicator(LexicalEntity): pass
class LexicalGroupEnd(LexicalEntity): pass