import glob
import json

import os
from json import JSONEncoder

import thinglang
from thinglang.compiler import Opcode
from thinglang.foundation import templates
from thinglang.lexer.tokens import LexicalToken
from thinglang.lexer.tokens.base import LexicalIdentifier
from thinglang.symbols.symbol import Symbol
from thinglang.utils.singleton import Singleton

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SEARCH_PATTERN = os.path.join(CURRENT_PATH,  'source/**/*.thing')
SYMBOLS_TARGET = os.path.join(CURRENT_PATH, 'symbols')
TYPES_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'types')
CORE_TYPES_TARGET = os.path.join(TYPES_TARGET, 'core')
EXECUTION_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'execution')


class JSONSerializer(JSONEncoder):
    def default(self, o):
        if isinstance(o, LexicalToken):
            return o.transpile()
        return super().default(o)


class Foundation(object, metaclass=Singleton):

    INTERNAL_TYPE_ORDERING = {
        LexicalIdentifier("none"): 0,
        LexicalIdentifier("text"): 1,
        LexicalIdentifier("number"): 2,
        LexicalIdentifier("Output"): 3
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
            name_id = LexicalIdentifier(name)
            target_name = '{}Type'.format(name.capitalize())
            ast, map = thinglang.preprocess(contents, False)
            methods = ast.children[0].methods()

            with open(os.path.join(CORE_TYPES_TARGET, target_name + '.h'), 'w') as f:
                f.write(templates.FOUNDATION_HEADER.format(
                    name=name.capitalize(),
                    code=ast.transpile(),
                    file_name=target_name + '.h'))

            symbol_map = map[name_id]
            symbol_map.override_index(Foundation.INTERNAL_TYPE_ORDERING[name_id])

            for symbol in symbol_map:
                symbol.convention = Symbol.INTERNAL

            with open(os.path.join(SYMBOLS_TARGET, name + '.thingsymbols'), 'w') as f:

                json.dump(symbol_map.serialize(), f, cls=JSONSerializer, indent=4, sort_keys=True)

            self.types[LexicalIdentifier(name.replace('_instance', ''))] = [x.name.transpile() for x in methods]

    @classmethod
    def write_type_enum(cls):
        with open(os.path.join(TYPES_TARGET, 'InternalTypes.h'), 'w') as f:
            f.write(cls.generate_enum('InternalTypes', list(Foundation.INTERNAL_TYPE_ORDERING.items())))

    @classmethod
    def write_opcode_enum(cls):
        with open(os.path.join(EXECUTION_TARGET, 'Opcodes.h'), 'w') as f:
            f.write(cls.generate_enum('Opcode', Opcode.all()))

    @classmethod
    def generate_enum(cls, cls_name, values):
        code = templates.FOUNDATION_ENUM.format(
            name=cls_name,
            values=',\n'.join('    {} = {}'.format(option[0].upper(), option[1]) for option in values),
            file_name=cls_name + '.h'
        ) + templates.FOUNDATION_SWITCH.format(
            name=cls_name,
            func_name="describe",
            cases='\n'.join(templates.ENUM_CASE.format(enum_class=cls_name, name=option[0].upper(), value='"{}"'.format(option[0].upper())) for option in values),
        )

        if not hasattr(values[0], '_fields'):
            return code

        for arg in getattr(values[0], '_fields')[2:]:
            code += templates.FOUNDATION_SWITCH.format(
                name=cls_name,
                func_name=arg,
                cases='\n'.join(templates.ENUM_CASE.format(enum_class=cls_name, name=option[0].upper(), value=getattr(option, arg)) for option in values),
            )

        return code

    def generate_code(self):
        self.generate_types()
        self.write_type_enum()
        self.write_opcode_enum()

    @classmethod
    def format_internal_type(self, type):
        name = type.value.capitalize()
        return '{}Namespace::{}Instance'.format(name, name)


if __name__ == "__main__":
    Foundation()
