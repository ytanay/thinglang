#pragma once

#include "../../utils/TypeNames.h"


class ConsoleType : public ThingTypeInternal {

	// TODO: make sure constructor cannot be called

    public:
    ConsoleType() : ThingTypeInternal({ nullptr, &write, &print, &print_format, &read_line }) {}; // constructor

	static void write();
	static void print();
    static void print_format();
	static void read_line();
    
};
