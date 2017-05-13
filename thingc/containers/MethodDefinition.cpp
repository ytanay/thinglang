#include "MethodDefinition.h"


void MethodDefinition::execute()
{
	for (auto symbol : this->symbols) {
		symbol.execute();
	};
}
