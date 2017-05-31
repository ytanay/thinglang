import glob

import os

import thinglang
from thinglang.foundation import templates
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.utils.singleton import Singleton

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SEARCH_PATTERN = os.path.join(CURRENT_PATH,  '**/*.thing')
TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'types')


class Foundation(object, metaclass=Singleton):

    TYPE_ORDERING = {
        "none": 0,
        "text": -1,
        "number": -2
    }

    def __init__(self):
        self.types = {}

        self.generate_code()

    def type(self, name):
        return self.types[name]

    def generate_types(self):
        for path in glob.glob(SEARCH_PATTERN, recursive=True):
            with open(path, 'r') as f:
                contents = f.read()

            name = os.path.basename(path).replace('.thing', '')
            target_name = '{}Instance'.format(name.capitalize())
            ast = thinglang.compiler(contents)
            methods = ast.children[0].methods()

            with open(os.path.join(TARGET, target_name + '.h'), 'w') as f:
                f.write(templates.FOUNDATION_HEADER.format(name.capitalize(), ast.transpile()))

            with open(os.path.join(TARGET, target_name + '.cpp'), 'w') as f:
                f.write(templates.FOUNDATION_SOURCE.format(name=name.capitalize(), methods=', '.join('&{}::{}'.format(target_name, method.name.transpile()) for method in methods)))

            self.types[LexicalIdentifier(name.replace('_instance', ''))] = [x.name.transpile() for x in methods]

    @staticmethod
    def generate_type_enum():
        with open(os.path.join(TARGET, 'InternalTypes.h'), 'w') as f:
            f.write(templates.FOUNDATION_ENUM.format(
                ', '.join('{} = {}'.format(name.upper(), idx) for name, idx in Foundation.TYPE_ORDERING.items())))

    def generate_code(self):
        self.generate_types()
        self.generate_type_enum()


if __name__ == "__main__":
    Foundation()
