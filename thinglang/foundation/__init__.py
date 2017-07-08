import glob

import os

import thinglang
from thinglang.compiler import OPCODES
from thinglang.foundation import templates
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.utils.singleton import Singleton

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SEARCH_PATTERN = os.path.join(CURRENT_PATH,  '**/*.thing')
TYPES_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'types')
CORE_TYPES_TARGET = os.path.join(TYPES_TARGET, 'core')
EXECUTION_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'execution')


class Foundation(object, metaclass=Singleton):

    INTERNAL_TYPE_ORDERING = {
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
            target_name = '{}Type'.format(name.capitalize())
            ast = thinglang.compiler(contents, executable=False)
            methods = ast.children[0].methods()

            with open(os.path.join(CORE_TYPES_TARGET, target_name + '.h'), 'w') as f:
                f.write(templates.FOUNDATION_HEADER.format(
                    name=name.capitalize(),
                    code=ast.transpile(),
                    file_name=target_name + '.h'))

            self.types[LexicalIdentifier(name.replace('_instance', ''))] = [x.name.transpile() for x in methods]

    @classmethod
    def write_type_enum(cls):
        with open(os.path.join(TYPES_TARGET, 'InternalTypes.h'), 'w') as f:
            f.write(cls.generate_enum('InternalTypes', Foundation.INTERNAL_TYPE_ORDERING))

    @classmethod
    def write_opcode_enum(cls):
        with open(os.path.join(EXECUTION_TARGET, 'Opcodes.h'), 'w') as f:
            f.write(cls.generate_enum('Opcode', OPCODES))

    @classmethod
    def generate_enum(cls, cls_name, values):
        return templates.FOUNDATION_ENUM.format(
            name=cls_name,
            values=',\n'.join('    {} = {}'.format(name.upper(), idx) for name, idx in values.items()),
            cases='\n'.join(templates.ENUM_CASE.format(enum_class=cls_name, name=name.upper()) for name in values),
            file_name=cls_name + '.h'
        )

    def generate_code(self):
        self.generate_types()
        self.write_type_enum()
        self.write_opcode_enum()


if __name__ == "__main__":
    Foundation()
