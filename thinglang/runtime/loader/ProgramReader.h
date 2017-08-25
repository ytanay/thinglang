#pragma once

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <utility>
#include <memory>

#include "../utils/TypeNames.h"

#include "../containers/Method.h"



class ProgramReader {
public:
    explicit ProgramReader(const std::string &filename) {
        auto f = new std::ifstream(filename, std::ios::in | std::ios::binary);
        if(!f->is_open()) {
            std::cerr << "Could not open file " << filename << std::endl;
            f = nullptr;
        }

        file = std::shared_ptr<std::ifstream>(f);
        }

    ProgramReader() {
        std::cerr << "Creating against cin" << std::endl;
        file = std::shared_ptr<std::istream>(&std::cin);
    }


    ProgramInfo process();

    void read_header();

    Things read_data();

    Thing read_data_block();

    Types read_code();

    Type read_class();

    Method read_method();

    Symbol read_symbol(Opcode opcode);


    template<typename T>
    T read() {
        T val;
        file->read(reinterpret_cast<char *>(&val), sizeof(T));
        index += sizeof(T);
        return val;
    }

    std::string read(Size size) {
        std::string val(size, '\0');
        file->read(&val[0], size);
        index += size;
        return val;
    }

    Size read_size() {
        return read<Size>();
    }

    Opcode read_opcode() {
        return static_cast<Opcode>(read<uint8_t>());
    }

    bool in_data() const {
        return index < data_size;
    }

    bool in_program() const {
        return index < program_size;
    }

private:
    std::shared_ptr<std::istream> file;
    Index index = 0, entry = 0;
    Size program_size = 0, data_size = 0;

    static const std::string EXPECTED_MAGIC;
    static const uint16_t EXPECTED_VERSION = 1;
};
