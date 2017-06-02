FOUNDATION_HEADER = """
#pragma once

#include "../execution/Program.h"
#include "../containers/ThingInstance.h"
#include "../utils/formatting.h"

namespace {}Namespace {{
{}
}}

""".strip()

FOUNDATION_SOURCE = """
#include "{name}Instance.h"

namespace {name}Namespace {{
    const std::vector<InternalMethod> {name}Instance::methods = {{{methods}}};
}}

""".strip()


FOUNDATION_ENUM = """
#pragma once

enum class InternalTypes {{
{}
}};
""".strip()


FOUNDATION_VIRTUALS = """
    virtual std::string text() const override {{
        return to_string({first_member});
    }}
    
    virtual void call_method(unsigned int target) override {{
        internals[target]();
    }}
"""