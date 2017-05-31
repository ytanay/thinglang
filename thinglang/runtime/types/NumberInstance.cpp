#include "NumberInstance.h"

namespace NumberNamespace {
    const std::vector<InternalMethod> NumberInstance::methods = {&NumberInstance::__LexicalAddition__, &NumberInstance::__LexicalMultiplication__};
}