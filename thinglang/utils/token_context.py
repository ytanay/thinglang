class TokenContext(object):

    def __init__(self, line, number):
        self.line, self.number = line.strip(), number + 1

    def __str__(self):
        return '<L{}> {}'.format(self.number, self.line)