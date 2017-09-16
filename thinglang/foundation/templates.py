HEADER = """/**
    {file_name}
    Auto-generated code - do not modify.
    thinglang C++ transpiler, 0.0.0
**/

"""


FOUNDATION_HEADER = HEADER + """
#pragma once

#include "../../utils/TypeNames.h"
#include "../../execution/Globals.h"
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


FOUNDATION_TYPE = """

class {instance_cls_name} : public BaseThingInstance {{
    
    public:
    explicit {instance_cls_name}() = default; // empty constructor
    explicit {instance_cls_name}({member_list}) : val(val) {{}}; // value constructor
    
    /** Mixins **/
    
    virtual std::string text() override {{
        return to_string(val);
    }}
    
    bool boolean() override {{
        return to_boolean(val);
    }}
    
    /** Members **/
    
    {members}
}};


typedef {instance_cls_name} this_type;

class {type_cls_name} : public ThingTypeInternal {{
    
    public:
    {type_cls_name}() : ThingTypeInternal({{ {method_list} }}) {{}}; // constructor
 
    {methods}
    
}};
"""


FOUNDATION_METHOD = """
    static {return_type} {name}({arguments}) {{
{preamble}
{body}
    }}
"""


FOUNDATION_ENUM = HEADER + """
#pragma once

#include <string>
#include "../errors/RuntimeError.h"

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


CONDITIONAL = """
        if({condition}) {{
{body}
        }}
"""


ELSE_CLAUSE = """
        else {{
{body}
    }}
"""

IMPLICIT_CONSTRUCTOR = """
    static Thing __constructor__() {
        return Thing(new this_type());
    }
"""

ARGUMENT_POP_TYPE = '\t\tauto {name} = Program::argument<{type}>();'
ARGUMENT_POP_GENERIC = '\t\tauto {name} = Program::pop();'

RETURN_VALUE = "return {value};"
RETURN_VALUE_INSTANTIATE = 'return Thing(new this_type({value}));'
RETURN_NULL = 'return nullptr;'


def format_internal_type_name(type):
    name = type.value.capitalize()
    return '{}Namespace::{}Instance'.format(name, name)


def get_names(name):
    name = name.transpile().capitalize()
    return '{}Type'.format(name), '{}Instance'.format(name)


