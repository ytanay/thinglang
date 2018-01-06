HEADER = """/**
    {file_name}
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/
"""


FOUNDATION_ENUM = HEADER + """
#pragma once

#include <string>

{imports}

enum class {name} {{
{values}
}};

"""


FOUNDATION_SWITCH = """
inline auto {func_name}({name} val){{
    switch (val){{
        {cases}
    }}
}}
"""


ENUM_CASE = """
        case {enum_class}::{name}:
            return {value};"""


TYPE_INSTANTIATION = HEADER + """
{imports}

enum PrimitiveType {{
    {primitives}
}};

inline InternalType get_type(const std::string& type_name){{
    {conditions}
    
    throw RuntimeError("Unknown type name: " + type_name);  
}}
"""


TYPE_CONDITIONAL = """if(type_name == "{name}") return singleton<{cls_name}>();"""


def class_names(name):
    name = name.serialize()
    formatted_name = name[0].upper() + name[1:]
    return '{}Type'.format(formatted_name), '{}Instance'.format(formatted_name)
