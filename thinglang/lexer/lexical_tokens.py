from thinglang.common import Describable, ValueType, ImmediateValue, ResolvableValue


class LexicalEntity(Describable):
    EMITTABLE = True

    def __init__(self, raw):
        self.raw = raw

    @classmethod
    def next_operator_set(cls, current, original):
        return current

    def contextify(self, context):
        self.context = context
        return self


# Derived types
class LexicalAccess(LexicalEntity):
    pass  # a.b

class LexicalParenthesesOpen(LexicalEntity): pass # (
class LexicalParenthesesClose(LexicalEntity): pass # )


class LexicalQuote(LexicalEntity): # "
    EMITTABLE = False

    @classmethod
    def next_operator_set(cls, current, original):
        if current is original:
            return {'"': LexicalQuote}
        return original

class LexicalSeparator(LexicalEntity): pass # ,

class LexicalIndent(LexicalEntity): pass # <TAB>

class LexicalAssignment(LexicalEntity): pass


class LexicalBinary(LexicalEntity):
    def __init__(self, operator):
        super(LexicalBinary, self).__init__(operator)
        self.operator = operator


class FirstOrderLexicalBinary(LexicalBinary): pass
class SecondOrderLexicalBinary(LexicalBinary): pass


class LexicalIdentifier(LexicalEntity, ResolvableValue):
    def __init__(self, value):
        super(LexicalIdentifier, self).__init__(value)
        self.value = value

    def describe(self):
        return self.value

    def evaluate(self, stack):
        return stack[self.value]


class LexicalNumericalValue(LexicalEntity, ImmediateValue):
    def __init__(self, value):
        super(LexicalNumericalValue, self).__init__(value)
        self.value = int(value)

    def evaluate(self, stack):
        return self.value


class LexicalDeclarationThing(LexicalEntity): pass
class LexicalDeclarationMethod(LexicalEntity): pass
class LexicalArgumentListIndicator(LexicalEntity): pass
class LexicalGroupEnd(LexicalEntity): pass
class LexicalInlineComment(LexicalEntity): pass
class LexicalReturnStatement(LexicalEntity): pass