#include "ProgramReader.h"
#include "../types/InternalTypes.h"
#include "../errors/RuntimeError.h"
#include "../types/core/TextType.h"
#include "../types/core/NumberType.h"
#include "../execution/Program.h"

const std::string ProgramReader::MAGIC = "THING";

ProgramInfo ProgramReader::process() {
    read_header();

    auto data = read_data();
    auto code = read_code();
    return ProgramInfo(entry, data, code);
}

void ProgramReader::read_header() {
    if (!file) {
        throw RuntimeError("Cannot open file");
    }

    auto magic = read(MAGIC.size());

    if (magic != MAGIC) {
        throw RuntimeError("Invalid file format");
    }

    auto version = read<uint16_t>();
    program_size = read<uint32_t>();
    data_size = read<uint32_t>();
    entry = read<uint32_t>();
    index = 0; // reset the index, since the program_size in the header does not include the header itself

    std::cerr << "thinglang bytecode version: " << version << ", total size: " << program_size << ", data size: "
              << data_size << ", entry point: " << entry << std::endl;
}

Things ProgramReader::read_data() {
    std::cerr << "Reading data section..." << std::endl;

    Things static_data;

    while (in_data()) {
        static_data.push_back(read_data_block());
    }

    return static_data;

}


Thing ProgramReader::read_data_block() {
    auto type = static_cast<InternalTypes>(read<int32_t>());

    switch (type) {
        case InternalTypes::TEXT: {
            auto size = read_size();
            auto data = read(size);
            std::cerr << "\tReading text (" << size << " bytes): " << data << std::endl;
            auto instance = Program::type<TextNamespace::TextType>(type)->create();
            static_cast<TextNamespace::TextInstance*>(instance.get())->val = data;
            return instance;
        }
        case InternalTypes::NUMBER: {
            auto data = read<int32_t>();
            std::cerr << "\tReading int: " << data << std::endl;
            auto instance = Program::type<NumberNamespace::NumberType>(type)->create();
            static_cast<NumberNamespace::NumberInstance*>(instance.get())->val = data;
            return instance;
        }

        default:
            throw RuntimeError("Unknown static data type " + std::to_string(int(type)));

    }
}

Types ProgramReader::read_code() {
    std::cerr << "Reading program..." << std::endl;
    Types user_types;

    while (in_program()) {
        std::cerr << "\t[" << user_types.size() << "] ";
        user_types.push_back(read_class());
    }

    if (index != program_size) {
        throw RuntimeError(
                std::string("Index mismatch " + std::to_string(index) + ", " + std::to_string(program_size)).c_str());
    } else {
        std::cerr << "Program processed successfully" << std::endl << std::endl;
    }

    return user_types;
}


Type ProgramReader::read_class() {
    assert(read_opcode() == Opcode::THING_DEFINITION);

    auto member_count = read_size();
    auto method_count = read_size();
    std::cerr << "Encountered class of " << member_count << " members and " << method_count << " methods"
              << std::endl;
    std::vector<Method> methods;

    for (int i = 0; i < method_count; i++) {
        std::cerr << "\t[" << methods.size() << "] ";
        methods.push_back(read_method());
    }
    return new ThingTypeExternal("Unknown class", "", methods);

}

Method ProgramReader::read_method() {
    assert(read_opcode() == Opcode::METHOD_DEFINITION);

    uint32_t frame_size = read_size();
    uint32_t arguments = read_size();

    std::cerr << "Encountered method (frame size=" << frame_size << ", args=" << arguments << ")" << std::endl;
    std::vector<Symbol> symbols;

    for (auto opcode = read_opcode(); opcode != Opcode::METHOD_END; opcode = read_opcode()) {
        auto symbol = read_symbol(opcode);

        std::cerr << "\t\t\tReading symbol [" << symbols.size() << "] " << describe(opcode) << " (" << symbol.target << ", " << symbol.secondary
                  << ")" << std::endl;

        symbols.push_back(symbol);
    }

    return Method(frame_size, arguments, symbols);
}

Symbol ProgramReader::read_symbol(Opcode opcode) {
    switch (arg_count(opcode)) {
        case 0:
            return Symbol(opcode);

        case 1:
            return Symbol(opcode, read_size());

        case 2: {
            auto target = read_size();
            auto value = read_size();
            return Symbol(opcode, target, value);
        }

        default:
            throw RuntimeError(std::string("Unparsable symbol ") + describe(opcode));
    }
}
