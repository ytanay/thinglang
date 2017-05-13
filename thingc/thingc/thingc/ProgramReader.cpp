#include "ProgramReader.h"


const std::string ProgramReader::MAGIC = "THING";

ProgramInfo ProgramReader::process()
{
	read_header();

	auto data = read_data();
	auto code = read_code();
	return ProgramInfo(data, code);
}

void ProgramReader::read_header()
{
	if (!file.is_open()) {
		throw std::exception("Cannot open file");
	}

	auto magic = read(MAGIC.size());

	if (magic != MAGIC) {
		throw std::exception("Invalid file format");
	}

	auto version = read<uint16_t>();
	program_size = read<uint32_t>();
	data_size = read<uint32_t>();
	index = 0; // reset the index, since the program_size in the header does not include the header itself

	std::cerr << "thinglang bytecode version: " << version << ", total size: " << program_size << ", data size: " << data_size << std::endl;
}

std::vector<PThingInstance> ProgramReader::read_data() {
	std::cerr << "Reading data section..." << std::endl;

	std::vector<PThingInstance> static_data;

	while (in_data()) {
		static_data.push_back(read_data_block());
	}

	return static_data;

}


PThingInstance ProgramReader::read_data_block() {
	auto type = read<int32_t>();

	switch (type) {
	case -1: {
		auto size = read_size();
		auto data = read(size);
		std::cerr << "\tReading text (" << size << " bytes): " << data << std::endl;
		return PThingInstance(new TextInstance(data));
	}
	case -2: {
		auto data = read<int32_t>();
		std::cerr << "\tReading int: " << data << std::endl;
		return PThingInstance(new NumberInstance(data));
	}

	default:
		throw std::exception("Unknown static data type");

	}
}

std::vector<TypeInfo> ProgramReader::read_code() {
	

	std::cerr << "Reading program..." << std::endl;
	std::vector<TypeInfo> user_types;

	while (in_program()) {
		auto class_definition_size = read_size();
		std::cerr << "\tEncountered class (id=" << (user_types.size() - 1) << ") of size " << class_definition_size << std::endl;
		user_types.push_back(read_class(class_definition_size));
	}

	if (index != program_size) {
		throw std::exception(std::string("Index mismatch " + std::to_string(index) + ", " + std::to_string(program_size)).c_str());
	}
	else {
		std::cerr << "Program processed successfully" << std::endl << std::endl;
	}

	return user_types;
}


TypeInfo ProgramReader::read_class(uint32_t size) {
	uint32_t last_index = index + size;
	std::vector<MethodDefinition> methods;

	while (index < last_index) {
		auto method_size = read_size();
		methods.push_back(read_method(method_size));
	}
	return TypeInfo("Unknown class", "", methods);

}

MethodDefinition ProgramReader::read_method(size_t size) {
	uint32_t frame_size = read_size();
	uint32_t arguments = read_size();
	uint32_t last_index = index + size;

	std::cerr << "\tEncountered method (size=" << size << ", frame size=" << frame_size << ", args=" << arguments << ")" << std::endl;
	std::vector<Symbol> symbols;


	while (index < last_index) {
		symbols.push_back(read_symbol());
	}

	return MethodDefinition(frame_size, arguments, symbols);
}

Symbol ProgramReader::read_symbol() {
	auto opcode = read_opcode();
	std::cerr << "\t\t\tReading symbol " << (int)opcode << std::endl;

	switch (opcode) {

	case Opcode::PUSH_CONST: {
		auto data_index = read_size();
		return Symbol(Opcode::PUSH_CONST, data_index);
	}

	case Opcode::PUSH: {
		auto data_index = read_size();
		return Symbol(Opcode::PUSH, data_index);
	}

	case Opcode::PRINT: {
		return Symbol(Opcode::PRINT);
	}

	case Opcode::CALL_INTERNAL: {
		return Symbol(Opcode::CALL_INTERNAL, read_size());
	}

	case Opcode::RETURN: {
		return Symbol(Opcode::RETURN);
	}

	case Opcode::CALL:
		return Symbol(Opcode::CALL, read_size());

	case Opcode::CALL_METHOD:
		return Symbol(Opcode::CALL_METHOD, read_size());

	default:
		throw std::exception(std::string("Unknown opcode " + std::to_string((int)opcode)).c_str());
	}
}
