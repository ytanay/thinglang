#include "ProgramReader.h"
const std::string ProgramReader::MAGIC = "THING";
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

