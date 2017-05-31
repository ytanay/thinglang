#include <iostream>
#include <algorithm>
#include "MethodDefinition.h"
#include "../execution/Program.h"


void MethodDefinition::execute() {
    Program::create_frame(frame_size);

    for (unsigned int i = 0; i < arguments; i++) {
        Program::frame()[i] = Program::pop();
    }

    for (int counter = 0; counter < symbols.size();) {
        auto symbol = symbols[counter];

        std::cerr << "[" << counter << "] Executing symbol " << describe(symbol.opcode) << ": " << symbol.target << ", "
                  << symbol.secondary << " -> [";
        std::for_each(Program::frame().begin(), Program::frame().end(),
                      [](const PThingInstance &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
        std::cerr << "] -> ";
        std::for_each(Program::static_data.begin(), Program::static_data.end(),
                      [](const PThingInstance &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
        std::cerr << "]" << std::endl;


        switch (symbol.opcode) {

            case Opcode::NOP:
                break;

            case Opcode::PUSH: {
                Program::push(Program::frame()[symbol.target]);
                break;
            };

            case Opcode::PUSH_NULL: {
                Program::push(NULL);
                break;
            }

            case Opcode::POP: {
                Program::pop();
                break;
            }

            case Opcode::SET_STATIC: {
                Program::frame()[symbol.target] = Program::data(symbol.secondary);
                break;
            }

            case Opcode::SET: {
                Program::frame()[symbol.target] = Program::pop();
                break;
            }

            case Opcode::PUSH_STATIC: {
                Program::push(Program::data(symbol.target));
                break;
            }

            case Opcode::CALL: {
                auto instance = Program::top();
                instance->call_method(symbol.target);

                break;
            }

            case Opcode::CALL_METHOD: {
                auto instance = Program::instance();
                instance->call_method(symbol.target);
                break;
            }

            case Opcode::PRINT:
                std::cout << Program::pop()->text() << std::endl;
                break;

            case Opcode::CALL_INTERNAL: {
                Program::internals[symbol.target]->call_internal(symbol.secondary);
                break;
            }

            case Opcode::RETURN: {
                Program::pop_frame();
                break;
            }

            case Opcode::JUMP: {
                counter = symbol.target;
                continue;
            }

            case Opcode::CONDITIONAL_JUMP: {
                auto value = Program::pop();
                if (!value) {
                    counter = symbol.target;
                    continue;
                }
                break;
            }

            default:
                throw RuntimeError(
                        "Cannot handle symbol " + describe(symbol.opcode) + " (" + std::to_string((int) symbol.opcode) +
                        ")");
        }


        counter++;
    };
}

