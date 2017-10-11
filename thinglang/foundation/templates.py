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


{code}
""".strip()


FOUNDATION_SOURCE = HEADER + """

{code}

""".strip()


FOUNDATION_TYPE_DECLARATION = """

class {instance_cls_name} : public BaseThingInstance {{
    
    public:
    explicit {instance_cls_name}() = default; // empty constructor
    
    {constructors}
    
    /** Mixins **/
    {mixins}
    
    /** Members **/
    {members}
}};


class {type_cls_name} : public ThingTypeInternal {{
    
    public:
    {type_cls_name}() : ThingTypeInternal({{ {method_list} }}) {{}}; // constructor
 
{methods}
    
}};
"""

FOUNDATION_TYPE_DEFINITION = """
#include "../InternalTypes.h"

/**
Methods of {type_cls_name}
**/

{methods}

/**
Mixins of {instance_cls_name}
**/
{mixins}
"""


FOUNDATION_METHOD = """
{return_type} {class_name}::{name}({arguments}) {{
{preamble}
{body}
    }}
"""

FOUNDATION_MIXINS_DECLARATION = """
    virtual std::string text() override;
    virtual bool boolean() override;
"""

FOUNDATION_MIXINS_DEFINITION = """
std::string {instance_cls_name}::text() {{
    return to_string({first_member});
}}

bool {instance_cls_name}::boolean() {{
    return to_boolean({first_member});
}}
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
Thing {type_cls_name}::__constructor__() {{
    return Thing(new {instance_cls_name}());
}}
"""

ARGUMENT_POP_TYPE = '\t\tauto {name} = Program::argument<{type}>();'
ARGUMENT_POP_GENERIC = '\t\tauto {name} = Program::pop();'
ARGUMENT_INSTANTIATE_SELF = '\t\tauto self = std::static_pointer_cast<{cls}>(Thing(new {cls}()));'

RETURN_VALUE = "return {value};"
RETURN_VALUE_INSTANTIATE = 'return Thing(new {instance_cls_name}({value}));'
RETURN_NULL = 'return nullptr;'

FOUNDATION_VALUE_CONSTRUCTOR = 'explicit {instance_cls_name}({member_list}) : val(val) {{}}; // value constructor'


def format_internal_type_name(type):
    name = type.value.capitalize()
    return '{}Instance'.format(name)


def class_names(name):
    name = name.transpile().capitalize()
    return '{}Type'.format(name), '{}Instance'.format(name)


def format_member_list(members):
    return ', '.join('{} {}'.format(x.type.transpile(), x.name.transpile()) for x in members)


def format_value_constructor(instance_cls_name, member_list):
    return FOUNDATION_VALUE_CONSTRUCTOR.format(
        instance_cls_name=instance_cls_name,
        member_list=format_member_list(member_list),
        initializer=', '.join('{name}({name})'.format(name=name.name.transpile()) for name in member_list[:1])
    )