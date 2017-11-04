#pragma once

#include "../utils/TypeNames.h"
#include "../types/core/BoolType.h"

const Thing BOOL_FALSE = Program::permanent<BoolInstance>(false);
const Thing BOOL_TRUE = Program::permanent<BoolInstance>(true);