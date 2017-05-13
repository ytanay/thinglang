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
