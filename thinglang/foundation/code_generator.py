import glob
import json
import os

import thinglang
from thinglang.compiler import Opcode
from thinglang.foundation import templates, definitions
from thinglang.lexer.tokens import LexicalToken
from thinglang.symbols.symbol import Symbol
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.lexer.tokens.base import LexicalIdentifier

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATTERN = os.path.join(CURRENT_PATH,  'source/**/*.thing')
SYMBOLS_TARGET = os.path.join(CURRENT_PATH, 'symbols')
TYPES_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'types')
CORE_TYPES_TARGET = os.path.join(TYPES_TARGET, 'core')
EXECUTION_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'execution')


class JSONSerializer(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, LexicalToken):
            return o.transpile()
        return super().default(o)


def generate_types():
    for path in glob.glob(SOURCE_PATTERN, recursive=True):
        with open(path, 'r') as f:
            contents = f.read()

        name = os.path.basename(path).replace('.thing', '')
        name_id = LexicalIdentifier(name)
        target_name = '{}Type'.format(name.capitalize())
        ast = thinglang.preprocess(contents)
        symbols = SymbolMapper(ast)

        with open(os.path.join(CORE_TYPES_TARGET, target_name + '.h'), 'w') as f:
            f.write(templates.FOUNDATION_HEADER.format(
                name=name.capitalize(),
                code=ast.transpile(),
                file_name=target_name + '.h'))

        symbol_map = symbols[name_id]
        symbol_map.override_index(definitions.INTERNAL_TYPE_ORDERING[name_id])

        for symbol in symbol_map:
            symbol.convention = Symbol.INTERNAL

        with open(os.path.join(SYMBOLS_TARGET, name + '.thingsymbols'), 'w') as f:
            json.dump(symbol_map.serialize(), f, cls=JSONSerializer, indent=4, sort_keys=True)


def write_type_enum():
    with open(os.path.join(TYPES_TARGET, 'InternalTypes.h'), 'w') as f:
        f.write(generate_enum('InternalTypes', list(definitions.INTERNAL_TYPE_ORDERING.items())))


def write_opcode_enum():
    with open(os.path.join(EXECUTION_TARGET, 'Opcodes.h'), 'w') as f:
        f.write(generate_enum('Opcode', Opcode.all()))


def generate_enum(cls_name, values):
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


def generate_code():
    generate_types()
    write_type_enum()
    write_opcode_enum()


if __name__ == "__main__":
    generate_code()
