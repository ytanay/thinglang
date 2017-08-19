HEADER = """/**
    {file_name}
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

"""


FOUNDATION_HEADER = HEADER + """
#pragma once

#include "../../utils/TypeNames.h"
#include "../../utils/Formatting.h"
#include "../infrastructure/ThingType.h"
#include "../infrastructure/ThingInstance.h"
#include "../../execution/Program.h"

namespace {name}Namespace {{
{code}
}}

""".strip()

FOUNDATION_SOURCE = HEADER + """
#include "{name}Type.h"

namespace {name}Namespace {{
{methods}
}}

""".strip()


FOUNDATION_ENUM = HEADER + """
#pragma once

#include <string>
#include "../errors/RuntimeError.h"

enum class {name} {{
{values}
}};

"""


FOUNDATION_VIRTUALS = """
    Thing create(){{
        return Thing(new this_type());
    }}
"""


FOUNDATION_SWITCH = """
inline auto {func_name}({name} val){{
    switch (val){{
        {cases}
        
        default:
            throw RuntimeError("Unrecognized {name} in {func_name}");
    }}
}}
"""

ENUM_CASE = """
        case {enum_class}::{name}:
            return {value};"""


DEFAULT_CONSTRUCTOR = '\t{}() {{}};'


def format_internal_type(type):
    name = type.value.capitalize()
    return '{}Namespace::{}Instance'.format(name, name)
