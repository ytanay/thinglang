#include "ProgramReader.h"
#include "../types/core/TextType.h"

const std::string ProgramReader::EXPECTED_MAGIC = "THING\xCC";


ProgramInfo ProgramReader::process() {

    prepare_stream();
    read_header();

    auto code = read_code();
    auto data = read_data();
    auto source_map = read_source_map();
    auto source = read_source();

    return ProgramInfo(code, data, entry, source_map, source);
}

void ProgramReader::read_header() {

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


    std::cerr << "thinglang bytecode version: " << version << ", "
              << ", instruction count: " << instruction_count
              << ", data item count: " << data_item_count
              << ", entry point: " << entry << std::endl;
}


Types ProgramReader::read_code() {
    std::cerr << "Reading code section..." << std::endl;
    Types user_types;

    while (read_opcode() == Opcode::SENTINEL_THING_DEFINITION) {
        std::cerr << "\t[" << user_types.size() << "] ";
        user_types.push_back(read_class());
    }

    assert(last_opcode == Opcode::SENTINEL_CODE_END);

    if (instruction_counter != instruction_count) {
        throw RuntimeError(
                std::string("Index mismatch " + std::to_string(instruction_counter) + ", " + std::to_string(program_size)));
    } else {
        std::cerr << "Program processed successfully" << std::endl << std::endl;
    }

    return user_types;
}


Type ProgramReader::read_class() {

    auto member_count = read_size();
    auto method_count = read_size();
    std::cerr << "Encountered class of " << member_count << " members and " << method_count << " methods"
              << std::endl;
    std::vector<Method> methods;

    for (int i = 0; i < method_count; i++) {
        std::cerr << "\t[" << methods.size() << "] ";
        methods.push_back(read_method());
    }
    return new ThingTypeExternal("Unknown class", member_count, methods);

}

Method ProgramReader::read_method() {
    assert(read_opcode() == Opcode::SENTINEL_METHOD_DEFINITION);

    uint32_t frame_size = read_size();
    uint32_t arguments = read_size();

    std::cerr << "Encountered method (frame size=" << frame_size << ", args=" << arguments << ")" << std::endl;
    std::vector<Instruction> instructions;

    for (auto opcode = read_opcode(); opcode != Opcode::SENTINEL_METHOD_END; opcode = read_opcode()) {
        auto instruction = read_instruction(opcode);

        std::cerr << "\t\t\tReading instruction [" << instructions.size() << "] " << describe(opcode) << " (" << instruction.target << ", " << instruction.secondary
                  << ")" << std::endl;

        instructions.push_back(instruction);
    }

    return Method(frame_size, arguments, instructions);
}

Instruction ProgramReader::read_instruction(Opcode opcode) {
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
    std::cerr << "Reading data section..." << std::endl;

    Things static_data;

    for (int i = 0; i < data_item_count; i++){
        static_data.push_back(read_data_block());
    }

    assert(read_opcode() == Opcode::SENTINEL_DATA_END);

    return static_data;

}


Thing ProgramReader::read_data_block() {
    auto type = read_data_type();

    switch (type) {
        case InternalTypes::TEXT: {
            auto size = read_size();
            auto data = read_string(size);
            std::cerr << "\tReading text (" << size << " bytes): " << data << std::endl;
            auto instance = Program::type<TextNamespace::TextType>(type)->create();
            dynamic_cast<TextNamespace::TextInstance*>(instance.get())->val = data;
            return instance;
        }
        case InternalTypes::NUMBER: {
            auto data = read<int32_t>();
            std::cerr << "\tReading int: " << data << std::endl;
            auto instance = Program::type<NumberNamespace::NumberType>(type)->create();
            dynamic_cast<NumberNamespace::NumberInstance*>(instance.get())->val = data;
            return instance;
        }

        default:
            throw RuntimeError("Unknown static data type " + std::to_string(int(type)));

    }
}

void ProgramReader::prepare_stream() {

    assert(!file.is_open());

    file.open(filename, std::ios::in | std::ios::binary);

    if(!file.is_open()) {
        throw RuntimeError("Cannot open file");
    }

}

SourceMap ProgramReader::read_source_map() {
    auto refs = std::vector<Index>(instruction_count);

    for(int i = 0; i <instruction_count; i++){
        refs[i] = read<uint32_t>();
    }

    return refs;
}

Source ProgramReader::read_source() {
    Source lines;
    for (std::string line; std::getline(file, line); )
        lines.push_back(line);

    return lines;

}
