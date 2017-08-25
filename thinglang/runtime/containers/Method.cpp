#include <iostream>

#include "Method.h"
#include "../execution/Program.h"
#include "../types/infrastructure/ThingInstance.h"


void Method::execute() {
    std::cerr << "Entered method (stack frame size: " << frame_size << ")" << std::endl;
    Program::create_frame(frame_size);


    for (size_t i = 0; i < arguments; i++) {
        Program::frame()[arguments - i - 1] = Program::pop();
    }

    auto counter_end = symbols.size();


    for (Index counter = 0; counter < counter_end;) {
        auto symbol = symbols[counter];

        Program::status(counter, symbol);

        switch (symbol.opcode) {

            case Opcode::PASS:
                break;

            case Opcode::CALL: {
                Program::types[symbol.target]->call(symbol.secondary);
                break;
            }

            case Opcode::CALL_INTERNAL: {
                auto ret_val = Program::internals[symbol.target]->call(symbol.secondary);
                Program::push(ret_val);
                break;
            }

            case Opcode::INSTANTIATE: {
                auto new_thing = Thing(new ThingInstance(Program::types[symbol.target]->members));
                Program::frame()[0] = new_thing;
                Program::push(new_thing);
                break;
            }


            case Opcode::PUSH_LOCAL: {
                Program::push(Program::frame()[symbol.target]);
                break;
            };

            case Opcode::PUSH_STATIC: {
                Program::push(Program::data(symbol.target));
                break;
            }

            case Opcode::PUSH_MEMBER: {
                Program::push(Program::frame()[symbol.target]->get(symbol.secondary));
                break;
            }

            case Opcode::PUSH_NULL: {
                Program::push(nullptr);
                break;
            }

            case Opcode::POP: {
                Program::pop();
                break;
            }

            case Opcode::POP_LOCAL: {
                Program::frame()[symbol.target] = Program::pop();
                break;
            }

            case Opcode::ASSIGN_STATIC: {
                Program::frame()[symbol.target] = Program::data(symbol.secondary);
                break;
            }

            case Opcode::POP_MEMBER: {
                Program::frame()[symbol.target]->set(symbol.secondary, Program::pop());
                break;
            }

            case Opcode::DEREFERENCE: {
                Program::push(Program::pop()->get(symbol.target));
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

                if (!value || !value->boolean()) {
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
    std::cerr << "Exiting method" << std::endl;
}

