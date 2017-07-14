#include <iostream>

#include "MethodDefinition.h"
#include "../execution/Program.h"
#include "../types/infrastructure/ThingInstance.h"


void MethodDefinition::execute() {
    Program::create_frame(frame_size);

    for (size_t i = 0; i < arguments; i++) {
        Program::frame()[i] = Program::pop();
    }

    auto counter_end = symbols.size();


    for (Index counter = 0; counter < counter_end;) {
        auto symbol = symbols[counter];

        Program::status(counter, symbol);

        switch (symbol.opcode) {

            case Opcode::PASS:
                break;


            case Opcode::CALL: {
                if(symbol.secondary == 0){
                    Program::push(Thing(new ThingInstance));
                }

                Program::types[symbol.target]->call(symbol.secondary);
                break;
            }

            case Opcode::CALL_INTERNAL: {
                auto ret_val = Program::internals[symbol.target]->call(symbol.secondary);
                Program::push(ret_val);
                break;
            }

            case Opcode::PUSH: {
                Program::push(Program::frame()[symbol.target]);
                break;
            };

            case Opcode::PUSH_STATIC: {
                Program::push(Program::data(symbol.target));
                break;
            }

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

            case Opcode::RETURN: {
                counter = counter_end;
                continue;
            }

            case Opcode::JUMP: {
                counter = symbol.target;
                continue;
            }

            case Opcode::JUMP_CONDITIONAL: {
                auto value = Program::pop();
                if (!value) {
                    counter = symbol.target;
                    continue;
                }
                break;
            }

            default:
                throw RuntimeError(
                        std::string("Cannot handle symbol ") + describe(symbol.opcode) + " (" + std::to_string((int) symbol.opcode) +
                        ")");
        }


        counter++;
    };

    Program::pop_frame();
}

