HEADER = """/**
    {file_name}
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

"""


FOUNDATION_HEADER = HEADER + """
#pragma once

#include "../execution/Program.h"
#include "../containers/ThingInstance.h"
#include "../utils/formatting.h"

namespace {name}Namespace {{
{code}
}}

""".strip()

FOUNDATION_SOURCE = HEADER + """
#include "{name}Instance.h"

namespace {name}Namespace {{
    const std::vector<InternalMethod> {name}Instance::methods = {{
{methods}
    }};
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
    virtual std::string text() const override {{
        return to_string({first_member});
    }}
    
    virtual void call_method(unsigned int target) override {{
        methods[target]();
    }}
"""

ENUM_CASE = """
    case {enum_class}::{name}:
        return "{name}";"""

