class SourceReference(object):
    def __init__(self, filename, line_number, column_number):
        self.filename, self.line_number, self.column_number = filename, line_number, column_number


class SourceLine(object):
    """
    Represents a single line of code
    """

    def __init__(self, source, line_number, filename):
        self.source, self.line_number, self.filename = source.replace(' ' * 4, '\t').rstrip(), line_number, filename

    def __iter__(self):
        for column_number, char in enumerate(self.source):
            yield char, SourceReference(self.filename, self.line_number, column_number)

    @property
    def empty(self):
        return not self.source.strip()

    @classmethod
    def inline(cls, source):
        return cls(source, 0, '<inline>')


class SourceContext(object):
    """
    Wraps a single source file
    """

    def __init__(self, filename, override_source=None):
        self.filename = filename

        if override_source is not None:
            self.raw_contents = override_source.split('\n')
        else:
            with open(filename) as f:
                self.raw_contents = f.readlines()

        self.contents = [SourceLine(line, idx, filename) for idx, line in enumerate(self.raw_contents)]

    def __iter__(self):
        return iter(self.contents)

    @classmethod
    def wrap(cls, contents):
        return cls('<wrapped>', override_source=contents)
