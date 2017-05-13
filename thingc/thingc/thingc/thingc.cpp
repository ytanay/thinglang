#include <iostream>
#include <vector>
#include <fstream>


#include "ProgramReader.h"
#include "Program.h"


int main(int argc, char** argv) {
	
	if (argc != 2) {
		std::cerr << "Usage: thingc filename.thingc" << std::endl;
		return 1;
	}

	auto reader = ProgramReader(argv[1]);
	Program::load(reader.process());
	Program::start();


	return 0;
}

