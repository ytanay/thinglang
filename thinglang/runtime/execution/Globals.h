#pragma once

#include "../utils/TypeNames.h"
#include "../types/core/BoolType.h"

const Thing BOOL_FALSE = Thing(new BoolNamespace::BoolInstance(false));
const Thing BOOL_TRUE = Thing(new BoolNamespace::BoolInstance(true));