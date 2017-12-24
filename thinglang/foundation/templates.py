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

inline Type create_type(const std::string& type_name){{
    {conditions}
    
    throw RuntimeError("Unknown type name: " + type_name);  
}}
"""


TYPE_CONDITIONAL = """if(type_name == "{name}") return new {cls_name}();"""


def class_names(name):
    name = name.transpile().capitalize()
    return '{}Type'.format(name), '{}Instance'.format(name)
