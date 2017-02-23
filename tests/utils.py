INDENT = '\n' + ' ' * 8

def generate_simple_output_program(source):
    return """
thing Program
    does start{source}
    """.format(source=INDENT + INDENT.join([source] if isinstance(source, basestring) else source))