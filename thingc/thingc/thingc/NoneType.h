#pragma once

#include "TypeInfo.h"

class NoneType : public TypeInfo {
public:
	NoneType() : TypeInfo("None") {};

};

