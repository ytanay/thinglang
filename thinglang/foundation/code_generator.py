import glob
import json
import os

from thinglang import pipeline
from thinglang.compiler.opcodes import Opcode
from thinglang.foundation import templates, definitions
from thinglang.lexer.lexical_token import LexicalToken
from thinglang.lexer.values.identifier import GenericIdentifier
from thinglang.symbols.symbol import Symbol
from thinglang.symbols.symbol_mapper import SymbolMapper
from thinglang.utils.source_context import SourceContext

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SYMBOLS_TARGET = os.path.join(CURRENT_PATH, 'symbols')
TYPES_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'types')
CORE_TYPES_TARGET = os.path.join(TYPES_TARGET, 'core')
EXECUTION_TARGET = os.path.join(CURRENT_PATH, '..', 'runtime', 'execution')


class JSONSerializer(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, GenericIdentifier):
            return o.serialize()
        if isinstance(o, LexicalToken):
            return o.transpile()
        return super().default(o)


def generate_types():
    """
    Generates and writes the C++ code for internal thing types, such as the text and number classes
    Additionally, writes the symbol maps for the generated types
    """

    for name, path in definitions.INTERNAL_SOURCES.items():
        ast = pipeline.preprocess(SourceContext(path))
        symbol_map = SymbolMapper(ast)[name]
        symbol_map.convention = Symbol.INTERNAL

        for symbol in symbol_map:
            symbol.convention = Symbol.INTERNAL

        write_if_changed(os.path.join(SYMBOLS_TARGET, f'{name}.thingsymbols'), json.dumps(
            symbol_map.serialize(),
            cls=JSONSerializer,
            indent=4, sort_keys=True)
        )


def write_type_enum():
    """
    Create the internal types ordering enum
    """
    target_file = os.path.abspath(os.path.join(TYPES_TARGET, 'InternalTypes.h'))

    internal_types = {name: (path, templates.class_names(name)[0]) for name, path in definitions.INTERNAL_SOURCES.items()}
    imports = '\n'.join('#include "{}"'.format(relative_path(target_file, path, cls_name + '.h')) for name, (path, cls_name) in internal_types.items())

    write_if_changed(target_file, templates.TYPE_INSTANTIATION.format(
        file_name='InternalTypes.h',
        imports=imports,
        primitives=', '.join(x.upper() for x in definitions.PRIMITIVE_TYPES),
        conditions='\n    '.join(templates.TYPE_CONDITIONAL.format(name=name, cls_name=cls_name) for name, (path, cls_name) in internal_types.items())
    ))


def write_opcode_enum():
    """
    Creates the opcode enum used by the runtime
    """
    write_if_changed(os.path.join(EXECUTION_TARGET, 'Opcodes.h'), generate_enum('Opcode', Opcode.all()))


def generate_enum(cls_name, values, imports='') -> str:
    """
    Helper function to create C++ enum headers
    :param cls_name: the name of the enum
    :param values: values to include
    :param imports: additional files to import
    """
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
    """
    Writes a file to the disk if it does not exist or if it has changed since the last write
    """
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            if f.read() == contents:
                return

    with open(file_path, 'w') as f:
        f.write(contents)


def generate_code():
    """
    Calls all code generating functions
    """
    generate_types()
    write_type_enum()
    write_opcode_enum()


def relative_path(source, destination, file_name):
    relative = os.path.relpath(os.path.dirname(destination), os.path.dirname(source))
    return os.path.join(relative, file_name)

if __name__ == "__main__":
    generate_code()
