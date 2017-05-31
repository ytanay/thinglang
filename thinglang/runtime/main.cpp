#include <iostream>
#include <vector>
#include <fstream>

#include "errors/RuntimeError.h"
#include "execution/Program.h"
#include "loader/ProgramReader.h"


int main(int argc, char **argv) {

    if (argc != 2) {
        std::cerr << "Usage: thingc filename.thingc" << std::endl;
        return 1;
    }

    auto filename = std::string(argv[1]);

    if(filename == "--build-only"){
        std::cerr << "Build completed, not executing." << std::endl;
        return 0;
    }

    auto reader = filename == "-" ? ProgramReader() : ProgramReader(filename);

    try {
        auto info = reader.process();
        Program::load(info);
        Program::start();
    } catch (const RuntimeError &err) {
        std::cerr << "Error during execution: " << err.what() << std::endl;
        return 1;
    }

    return 0;
}
