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

enum class {name} {{
{values}
}};

inline std::string describe({name} val){{
     switch (val){{
        {cases}
    }}

}}
""".strip()


FOUNDATION_VIRTUALS = """
    Thing create(){{
        return Thing(new this_type());
    }}
"""

ENUM_CASE = """
    case {enum_class}::{name}:
        return "{name}";"""


DEFAULT_CONSTRUCTOR = '\t{}() {{}};'
