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


def class_names(name):
    name = name.transpile().capitalize()
    return '{}Type'.format(name), '{}Instance'.format(name)
