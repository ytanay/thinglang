import struct


class SourceContext(object):
    """
    Wraps a single source file
    """

    def __init__(self, filename, override_source=None):
        self.filename = filename

        self.raw_contents = override_source

        if self.raw_contents is None:
            with open(filename) as f:
                self.raw_contents = f.read()

        self.contents = [SourceLine(line, idx, filename) for idx, line in enumerate(self.raw_contents.split('\n'))]

    def __iter__(self):
        return iter(self.contents)

    @classmethod
    def wrap(cls, contents):
        return cls('<wrapped>', override_source=contents)


class SourceLine(object):
    """
    Wraps a single line of code
    """

    def __init__(self, source, line_number, filename):
        self.source, self.line_number, self.filename = source.replace(' ' * 4, '\t').rstrip(), line_number, filename

    def __iter__(self):
        for column_number, char in enumerate(self.source):
            yield char, SourceReference(self.filename, self.line_number, column_number, column_number + 1)

    @property
    def empty(self):
        return not self.source.strip()

    @classmethod
    def inline(cls, source):
        return cls(source, 0, '<inline>')


class SourceReference(object):
    """
    Refers to a slice of source code, from which a lexical token (or AST node) was derived.
    """

    def __init__(self, filename, line_number, column_start, column_end):
        self.filename, self.line_number, self.column_start, self.column_end = filename, line_number, column_start, column_end

    def __repr__(self):
        return '{}:{}:{}-{}'.format(self.filename, self.line_number, self.column_start, self.column_end)

    def __sub__(self, other):
        assert self.filename == other.filename and self.line_number == other.line_number and self.column_start >= other.column_start
        return SourceReference(self.filename, self.line_number, other.column_start, self.column_start)

    def __add__(self, other):
        assert isinstance(other, int)
        return SourceReference(self.filename, self.line_number, self.column_start, self.column_end + other)

    def serialize(self):
        return struct.pack('<i', self.line_number)

    @classmethod
    def invalid(cls):
        return cls('<invalid>', -1, -1, -1)

    @classmethod
    def generated(cls, reason):
        return cls('<generated:{}>'.format(reason), -1, -1, -1)

    @classmethod
    def combine(cls, tokens):
        refs = [x.source_ref for x in tokens if hasattr(x, 'source_ref') and x.source_ref]

        if not refs:
            return None

        assert len(set(x.filename for x in refs)) == len(set(x.line_number for x in refs)) == 1
        return cls(refs[0].filename, refs[0].line_number, min(x.column_start for x in refs), max(x.column_end for x in refs))