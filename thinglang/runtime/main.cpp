#include <iostream>
#include <vector>
#include <fstream>

#include "../include/args.h"

#include "errors/RuntimeError.h"
#include "execution/Program.h"
#include "loader/ProgramReader.h"


int main(const int argc, const char **argv)
{
    args::ArgumentParser parser("thinglang's runtime environment");
    args::HelpFlag help(parser, "help", "Display this help", {'h', "help"});
    args::Group group(parser, "", args::Group::Validators::Xor);
    args::Positional<std::string> filename(group, "file", "a file containing thinglang bytecode");
    args::Flag version(group, "version", "Prints the version and exits", {'v', "version"});

    try {
        parser.ParseCLI(argc, argv);
    } catch (args::Help) {
        std::cout << parser;
        return 0;
    } catch (args::Error e)  {
        std::cerr << e.what() << std::endl;
        std::cerr << parser;
        return 1;
    }

    if(version) {
        std::cerr << "thinglang runtime, version 0.0.0" << std::endl;
        return 0;
    }

    auto reader = ProgramReader(filename.Get());

    try {
        auto info = reader.process();
        Program::load(info);
        Program::start();
    } catch (const RuntimeError &err) {
        std::cerr << "Error during execution: " << err.what() << std::endl;
        return 1;
    }
}