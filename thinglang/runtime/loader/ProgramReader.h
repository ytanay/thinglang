#pragma once

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <utility>

#include "../types/TypeInfo.h"
#include "../types/NoneType.h"
#include "../types/TextInstance.h"
#include "../types/NumberInstance.h"

#include "../containers/MethodDefinition.h"

using PThingInstance = std::shared_ptr<ThingInstance>;
using ProgramInfo = std::pair<std::vector<PThingInstance>, std::vector<TypeInfo>>;

class ProgramReader {
public:
    ProgramReader(const std::string &filename) : file(filename, std::ios::in | std::ios::binary) {}

    ProgramInfo process();

    void read_header();

    std::vector<PThingInstance> read_data();

    PThingInstance read_data_block();

    std::vector<TypeInfo> read_code();

    TypeInfo read_class();

    MethodDefinition read_method();

    Symbol read_symbol(Opcode opcode);


    template<typename T>
    T read() {
        T val;
        file.read(reinterpret_cast<char *>(&val), sizeof(T));
        index += sizeof(T);
        return val;
    }

    std::string read(size_t size) {
        std::string val(size, '\0');
        file.read(&val[0], size);
        index += size;
        return val;
    }

    uint32_t read_size() {
        return read<uint32_t>();
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
    std::ifstream file;
    unsigned int index = 0;
    uint32_t program_size, data_size;

    static const std::string MAGIC;
};
