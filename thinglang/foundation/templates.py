"""
Templates used to generate C++ code for the runtime
"""

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
    
    {children}
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
        {epilogue}
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
        {prefix}if({condition}) {{
{body}
        }}
"""


ELSE_CLAUSE = """
        else {{
{body}
    }}
"""

IMPLICIT_CONSTRUCTOR = """
void {type_cls_name}::__constructor__() {{
    Program::push(Program::create<{instance_cls_name}>());
}}
"""

ARGUMENT_POP_TYPE = '\t\tauto {name} = Program::argument<{type}>();'
ARGUMENT_POP_GENERIC = '\t\tauto {name} = Program::pop();'
ARGUMENT_INSTANTIATE_SELF = '\t\tauto self = Program::create<{cls}>();'

RETURN_VALUE = "Program::push({value});"
RETURN_VALUE_INSTANTIATE = 'Program::push(Program::create<{instance_cls_name}>({value}));'
RETURN_NULL = 'return;'
RETURN_SELF = 'Program::push(self);'

FOUNDATION_VALUE_CONSTRUCTOR = 'explicit {instance_cls_name}({member_list}) : {initializer} {{}}; // value constructor'

FOUNDATION_CHILDREN = """
    Things& children() override {
        return val;
    }
"""


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