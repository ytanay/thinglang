#include "Program.h"
#include "../errors/Aborts.h"
#include "../types/InternalTypes.h"
#include "../execution/Instruction.h"

ThingStack Program::stack;
FrameStack Program::frames;
Things Program::static_data;
Index Program::entry = 0;
Index Program::initial_frame_size = 0;
SourceMap Program::source_map;
Source Program::source;
InstructionList Program::instructions;

Types Program::internals = {
        nullptr,
        new TextType(),
        new NumberType(),
        new BoolType(),
        new ListType(),
        new ConsoleType(),
        new FileType()
};



Thing Program::pop() {
    if(stack.empty())
        critical_abort(EMPTY_PROGRAM_STACK);

    auto ti = static_cast<std::shared_ptr<BaseThingInstance> &&>(stack.top());
    stack.pop();
    return ti;
}

void Program::load(ProgramInfo &info) {
    auto loaded_code = static_cast<InstructionList &&>(std::get<0>(info));
    auto loaded_data = static_cast<Things &&>(std::get<1>(info));
    auto loaded_source_map = static_cast<SourceMap &&>(std::get<4>(info));
    auto loaded_source = static_cast<Source &&>(std::get<5>(info));

    entry = std::get<2>(info);
    initial_frame_size = std::get<3>(info);

    static_data.insert(static_data.end(), loaded_data.begin(), loaded_data.end());
    instructions.insert(instructions.end(), loaded_code.begin(), loaded_code.end());
    source_map.insert(source_map.end(), loaded_source_map.begin(), loaded_source_map.end());
    source.insert(source.end(), loaded_source.begin(), loaded_source.end());
}


void Program::status(Index counter, const Instruction& instruction) {
    auto source_idx = source_map[instruction.index];

    assert(source_idx < source.size());

    std::cerr << "[" << counter << "] Executing instruction " << describe(instruction.opcode) << ": " << instruction.target << ", "
              << instruction.secondary << " -> [";
    if(!Program::frames.empty())
        std::for_each(Program::frame().begin(), Program::frame().end(),
                      [](const Thing &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
    std::cerr << "] -> [" << trim(source[source_idx]) << "]" << std::endl;

}

void inline Program::copy_args(Size count, Size offset){
    for (size_t i = 0; i < count; i++) {
        Program::frame()[offset - i] = Program::pop();
    }
}

void Program::execute() {

    auto counter_end = instructions.size();

    std::stack<Index> return_stack;
    std::stack<Index> call_stack;

    return_stack.push(counter_end);
    call_stack.push(entry);

    Program::create_frame(initial_frame_size);

    std::cerr << "Starting execution (upper boundary " << counter_end << ")" << std::endl;
    for (Index counter = entry; counter < counter_end;) {
        handle_instruction:

        auto instruction = instructions[counter];

        Program::status(counter, instruction);

        switch (instruction.opcode) {

            case Opcode::PASS:
                break;

            case Opcode::CALL: {
                return_stack.push(counter + 1);
                call_stack.push(instruction.target);
                Program::create_frame(instruction.secondary);
                counter = instruction.target;

                goto handle_instruction;
            }

            case Opcode::CALL_INTERNAL: {

                auto ret_val = Program::internals[instruction.target]->call(instruction.secondary);
                Program::push(ret_val);
                break;
            }

            case Opcode::INSTANTIATE: {
                auto new_thing = Thing(new ThingInstance(instruction.secondary));
                Program::frame()[0] = new_thing;
                Program::copy_args(instruction.target, instruction.target);
                Program::push(new_thing);
                break;
            }

            case Opcode::ARG_COPY: {
                Program::copy_args(instruction.target, instruction.target - 1);
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
                counter = return_stack.top();
                return_stack.pop();
                call_stack.pop();
                continue; // Not goto handle_instruction because this may be the program end
            }

            case Opcode::THROW: {

                while(!call_stack.empty()){

                    // Look for an exception handler which matches the exception we are throwing.
                    for(Index i = call_stack.top() - 1; instructions[i].opcode != Opcode::SENTINEL_METHOD_DEFINITION; i -= 2){
                        auto range = instructions[i], definition = instructions[i - 1];

                        if(definition.secondary == instruction.target && counter >= range.target && counter <= range.secondary){
                            counter = definition.target;
                            goto handle_instruction;
                        }
                    }

                    // If we couldn't find any, walk up the call stack
                    counter = return_stack.top() - 1;

                    Program::pop_frame();
                    call_stack.pop();
                    return_stack.pop();

                }

                critical_abort(UNHANDLED_EXCEPTION);

            }

            case Opcode::JUMP: {
                counter = instruction.target;
                goto handle_instruction;
            }

            case Opcode::JUMP_CONDITIONAL: {
                auto value = Program::pop();

                if (!value || !value->boolean()) {
                    counter = instruction.target;
                    goto handle_instruction;
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

    std::cerr << "Program execution ended" << std::endl;

}


