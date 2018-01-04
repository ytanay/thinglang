#include <cassert>
#include "ProgramReader.h"
#include "../utils/Formatting.h"
#include "../execution/Globals.h"

const std::string ProgramReader::EXPECTED_MAGIC = "THING\xCC";


ProgramInfo ProgramReader::process() {
    /**
     * Process a compile thinglang program
     */
    prepare_stream();
    read_header();

    auto imports = read_imports();
    //auto types = read_types();
    auto code = read_code();
    auto data = read_data();
    auto source_map = read_source_map();
    auto source = read_source();

    return ProgramInfo({code.first, data, code.second, imports, entry, initial_frame_size, source_map, source});
}

void ProgramReader::read_header() {
    /**
     * Reads the program header and performs basic sanity checks
     */

    auto magic = read_string(EXPECTED_MAGIC.size());

    if (magic != EXPECTED_MAGIC) {
        throw RuntimeError("Invalid file format");
    }

    auto version = read<uint16_t>();

    if (version != EXPECTED_VERSION){
        throw RuntimeError("Invalid bytecode version (" + to_string(version) + ")");
    }

    instruction_count = read<uint32_t>();
    data_item_count = read<uint32_t>();
    entry = read<uint32_t>();
    initial_frame_size = read<uint32_t>();


    std::cerr << "thinglang bytecode version: " << version
              << ", instruction count: " << instruction_count
              << ", data item count: " << data_item_count
              << ", entry point: " << entry << std::endl;
}


InternalTypeList ProgramReader::read_imports() {
    std::cerr << "Reading import table..." << std::endl;

    InternalTypeList type_list;
    while(read_opcode() == Opcode::SENTINEL_IMPORT_TABLE_ENTRY) {
        auto size = read_size();
        auto name = read_string(size);
        std::cerr << "\tImporting " << name << std::endl;
        type_list.push_back(get_type(name));
    }

    assert(last_opcode == Opcode::SENTINEL_IMPORT_TABLE_END);

    return type_list;
}


std::pair<InstructionList, UserTypeList> ProgramReader::read_code() {
    /**
     * Process the code section
     */
    std::cerr << "Reading code section..." << std::endl;
    InstructionList instructions;
    UserTypeList user_types;

    instruction_counter = 0;

    for(Opcode opcode = read_opcode(); opcode != Opcode::SENTINEL_CODE_END; opcode = read_opcode()) {
        auto instruction = read_instruction(opcode);

        if(instruction.opcode == Opcode::SENTINEL_THING_DEFINITION){
            std::cerr << "\tClass boundary (address=" << instructions.size() << ", members=" << instruction.target << ", NONE=" << instruction.secondary << ")" << std::endl;
            user_types.emplace_back(instruction.target, instruction.secondary);
        } else if(instruction.opcode == Opcode::SENTINEL_THING_EXTENDS) {
            assert(user_types.back().methods.empty());
            auto prior = user_types[instruction.target].methods;
            std::cerr << "\t\tClass extends " << instruction.target << ", adding " << prior.size() << " entries" <<std::endl;
            user_types.back().methods.insert(user_types.back().methods.end(), prior.begin(), prior.end());
        } else if(instruction.opcode == Opcode::SENTINEL_METHOD_DEFINITION){
            std::cerr << "\t\tMethod boundary (address=" << instruction.target << ", frame size=" << instruction.target << ", arguments=" << instruction.secondary << ")" << std::endl;
            user_types.back().methods.push_back(MethodInfo{instruction.target, instruction.secondary});
        } else {
            std::cerr << "\t\t\t[" << instructions.size() << "] " << describe(opcode) << " (" << instruction.target << ", " << instruction.secondary
                      << ")" << std::endl;
        }

        instructions.push_back(instruction);

    }

    assert(last_opcode == Opcode::SENTINEL_CODE_END);

    if (instruction_counter != instruction_count) {
        throw RuntimeError(
                std::string("Index mismatch " + std::to_string(instruction_counter) + ", " + std::to_string(instruction_count)));
    } else {
        std::cerr << "Code section processed successfully" << std::endl << std::endl;
    }

    return std::make_pair(instructions, user_types);
}


Instruction ProgramReader::read_instruction(Opcode opcode) {
    /**
     * Reads and parses the next instruction
     */
    auto instruction_id = instruction_counter - 1;

    switch (arg_count(opcode)) {
        case 0:
            return {instruction_id, opcode};

        case 1:
            return {instruction_id, opcode, read_size()};

        case 2: {
            auto target = read_size();
            auto value = read_size();
            return {instruction_id, opcode, target, value};
        }

        default:
            throw RuntimeError(std::string("Invalid instruction argument count ") + describe(opcode));
    }
}


Things ProgramReader::read_data() {
    /**
     * Reads the static data section
     */
    std::cerr << "Reading data section..." << std::endl;

    Things static_data;

    for (int i = 0; i < data_item_count; i++){
        static_data.push_back(read_data_block());
    }

    assert(read_opcode() == Opcode::SENTINEL_DATA_END);

    std::cerr << "Data section processed successfully" << std::endl << std::endl;

    return static_data;
}


Thing ProgramReader::read_data_block() {
    /**
     * Reads the next data block
     */
    auto type = read_data_type();

    switch (type) {
        case PrimitiveType::TEXT: {
            auto size = read_size();
            auto data = read_string(size);
            std::cerr << "\tReading text (" << size << " bytes): " << data << std::endl;
            auto instance = Program::permanent<TextInstance>(data);
            return instance;
        }
        case PrimitiveType::NUMBER: {
            auto data = read<int32_t>();
            std::cerr << "\tReading int: " << data << std::endl;
            auto instance = Program::permanent<NumberInstance>(data);
            return instance;
        }

        case PrimitiveType::BOOL: {
            auto data = read<uint8_t >();
            assert(data == 0 || data == 1);
            std::cerr << "\tReading bool: " << data << std::endl;
            return data ? BOOL_TRUE : BOOL_FALSE;
        }

        default:
            throw RuntimeError("Unknown static data type " + std::to_string(int(type)));

    }
}

void ProgramReader::prepare_stream() {
    /**
     * Prepare the bytecode stream
     */

    assert(!file.is_open());

    file.open(filename, std::ios::in | std::ios::binary);

    if(!file.is_open()) {
        throw RuntimeError("Cannot open file");
    }

}

SourceMap ProgramReader::read_source_map() {
    /**
     * Reads the source map section
     */
    auto refs = std::vector<Index>(instruction_count);

    for(int i = 0; i <instruction_count; i++){
        refs[i] = read<uint32_t>();
    }

    return refs;
}

Source ProgramReader::read_source() {
    /**
     * Reads the inline source
     */
    Source lines;
    for (std::string line; std::getline(file, line); )
        lines.push_back(line);

    return lines;

}
