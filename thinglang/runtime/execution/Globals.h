#pragma once

#include "../utils/TypeNames.h"
#include "../types/core/BoolType.h"

const Thing BOOL_FALSE = Thing(new BoolInstance(false));
const Thing BOOL_TRUE = Thing(new BoolInstance(true));