#pragma once

#include "../utils/TypeNames.h"
#include "../../foundation/classes/types/BoolType.h"
#include "Program.h"

const Thing BOOL_FALSE = Program::permanent<BoolInstance>(false);
const Thing BOOL_TRUE = Program::permanent<BoolInstance>(true);