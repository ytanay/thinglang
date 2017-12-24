#pragma once

#include <string>
#include <utility>
#include <vector>
#include <iostream>
#include <fstream>
#include <utility>
#include <memory>

#include "../execution/Instruction.h"
#include "../utils/TypeNames.h"
#include "../types/InternalTypes.h"
#include "../execution/Opcodes.h"


class ProgramReader {
public:

    explicit ProgramReader(std::string filename) : filename(std::move(filename)) {}

    ProgramInfo process();

    void read_header();

    Types read_imports();
    InstructionList read_code();
    Instruction read_instruction(Opcode opcode);

    Things read_data();
    Thing read_data_block();

    template<typename T>
    T read() {
        T val;
        file.read(reinterpret_cast<char *>(&val), sizeof(T));
        return val;
    }

    std::string read_string(Size size) {
        std::string val(size, '\0');
        file.read(&val[0], size);
        return val;
    }

    Size read_size() {
        return read<Size>();
    }

    Opcode read_opcode() {
        last_opcode = static_cast<Opcode>(read<uint8_t>());
        instruction_counter++;
        return last_opcode;
    }

    PrimitiveType read_data_type(){
        return static_cast<PrimitiveType>(read<int32_t>());
    }


private:
    const std::string filename;
    std::ifstream file;
    Index entry = 0;

    Size program_size = 0, instruction_count = 0, data_item_count = 0, instruction_counter = 0, initial_frame_size = 0;

    Opcode last_opcode = Opcode::INVALID;

    static const std::string EXPECTED_MAGIC;
    static const uint16_t EXPECTED_VERSION = 3;

    void prepare_stream();

    SourceMap read_source_map();

    Source read_source();
};
