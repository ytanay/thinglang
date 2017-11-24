
class ParserRegistration(type):
    """
    Registers a class containing parsing rules
    """

    def __new__(mcs, name, bases, dct):
        mcs = super(ParserRegistration, mcs).__new__(mcs, name, bases, dct)

        mcs.RULES = sorted((value.__func__.parser_rule
                            for field, value in dct.items()
                            if hasattr(value, '__func__')
                            and hasattr(value.__func__, 'parser_rule')), key=lambda x: x.index)
        return mcs


class ParsingMixin(object, metaclass=ParserRegistration):
    """
    Implements the method testing whether a production rule of the grammar can be applied
    """

    @classmethod
    def propose_replacement(cls, tokens):
        for rule in cls.RULES:
            result = rule.matches(tokens)

            if result:
                return result

        return False
