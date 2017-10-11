import glob
import json
import os

from thinglang import pipeline
from thinglang.utils.source_context import SourceContext
from thinglang.compiler.opcodes import Opcode
from thinglang.foundation import templates, definitions
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.symbols.symbol import Symbol
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.lexer.values.identifier import Identifier

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

        name = os.path.basename(path).replace('.thing', '')
        name_id = Identifier(name)
        target_name = '{}Type'.format(name.capitalize())
        ast = pipeline.preprocess(SourceContext(path))
        symbols = SymbolMapper(ast)

        symbol_map = symbols[name_id]
        symbol_map.override_index(definitions.INTERNAL_TYPE_ORDERING[name_id])

        write_if_changed(os.path.join(CORE_TYPES_TARGET, target_name + '.cpp'), templates.FOUNDATION_SOURCE.format(
            name=name.capitalize(),
            code=ast.transpile(),
            file_name=target_name + '.cpp')
        )

        write_if_changed(os.path.join(CORE_TYPES_TARGET, target_name + '.h'), templates.FOUNDATION_HEADER.format(
            name=name.capitalize(),
            code=symbol_map.create_header(),
            file_name=target_name + '.h')
        )

        for symbol in symbol_map:
            symbol.convention = Symbol.INTERNAL

        write_if_changed(os.path.join(SYMBOLS_TARGET, name + '.thingsymbols'), json.dumps(
            symbol_map.serialize(),
            cls=JSONSerializer,
            indent=4, sort_keys=True)
        )


def write_type_enum():
    imports = '\n'.join('#include "core/{}.h"'.format(templates.class_names(name)[0]) for name in definitions.INTERNAL_TYPE_ORDERING)

    write_if_changed(os.path.join(TYPES_TARGET, 'InternalTypes.h'), generate_enum(
        'InternalTypes', list(definitions.INTERNAL_TYPE_ORDERING.items()), imports)
    )


def write_opcode_enum():
    write_if_changed(os.path.join(EXECUTION_TARGET, 'Opcodes.h'), generate_enum('Opcode', Opcode.all()))


def generate_enum(cls_name, values, imports=''):

    code = templates.FOUNDATION_ENUM.format(
        name=cls_name,
        values=',\n'.join('    {} = {}'.format(option[0].upper(), option[1]) for option in values),
        file_name=cls_name + '.h',
        imports=imports
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


def write_if_changed(file_path, contents):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            if f.read() == contents:
                return

    print('Writing {}'.format(file_path))

    with open(file_path, 'w') as f:
        f.write(contents)


def generate_code():
    generate_types()
    write_type_enum()
    write_opcode_enum()


if __name__ == "__main__":
    generate_code()
