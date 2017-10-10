#include <iostream>

#include "Method.h"
#include "../execution/Program.h"
#include "../types/infrastructure/ThingInstance.h"
#include "../errors/Aborts.h"


void Method::execute() {
    Program::create_frame(frame_size);

    std::cerr << "Reading " << arguments << " arguments at offset " << offset << std::endl;
    for (size_t i = 0; i < arguments; i++) {
        Program::frame()[offset - i] = Program::pop();
    }

    auto counter_end = instructions.size();


    for (Index counter = 0; counter < counter_end;) {
        auto instruction = instructions[counter];

        Program::status(counter, instruction);

        switch (instruction.opcode) {

            case Opcode::PASS:
                break;

            case Opcode::CALL: {
                Program::types[instruction.target]->call(instruction.secondary);
                break;
            }

            case Opcode::CALL_INTERNAL: {
                auto ret_val = Program::internals[instruction.target]->call(instruction.secondary);
                Program::push(ret_val);
                break;
            }

            case Opcode::INSTANTIATE: {
                auto new_thing = Thing(new ThingInstance(Program::types[instruction.target]->members));
                Program::frame()[0] = new_thing;
                Program::push(new_thing);
                break;
            }

            case Opcode::PUSH_LOCAL: {
                std::cerr << "\tPushing " << Program::frame()[instruction.target]->text() << std::endl;
                Program::push(Program::frame()[instruction.target]);
                break;
            };

            case Opcode::PUSH_STATIC: {
                Program::push(Program::data(instruction.target));
                break;
            }

            case Opcode::PUSH_MEMBER: {
                Program::push(Program::frame()[instruction.target]->get(instruction.secondary));
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
                Program::frame()[instruction.target] = Program::pop();
                break;
            }

            case Opcode::ASSIGN_STATIC: {
                Program::frame()[instruction.target] = Program::data(instruction.secondary);
                break;
            }

            case Opcode::POP_MEMBER: {
                Program::frame()[instruction.target]->set(instruction.secondary, Program::pop());
                break;
            }

            case Opcode::POP_DEREFERENCED: {
                auto container = Program::pop();
                auto value = Program::pop();
                container->set(instruction.target, value);
                break;
            }

            case Opcode::DEREFERENCE: {
                Program::push(Program::pop()->get(instruction.target));
                break;
            }

            case Opcode::RETURN: {
                Program::pop_frame();
                return;
            }

            case Opcode::THROW: {
                return;
            }

            case Opcode::JUMP: {
                counter = instruction.target;
                continue;
            }

            case Opcode::JUMP_CONDITIONAL: {
                auto value = Program::pop();

                if (!value || !value->boolean()) {
                    counter = instruction.target;
                    continue;
                }

                break;
            }

            default:
                throw RuntimeError(
                        std::string("Cannot handle instruction ") + describe(instruction.opcode) + " (" + std::to_string((int) instruction.opcode) +
                        ")");

        }


        counter++;
    };

    critical_abort(MISSING_RETURN);
}

