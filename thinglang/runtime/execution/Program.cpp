#include "Program.h"
#include "../types/InternalTypes.h"
#include "../execution/Instruction.h"
#include "../utils/Formatting.h"
#include "Globals.h"

ThingForwardList Program::stack;
FrameStack Program::frames;
ThingForwardList Program::objects;
unsigned char Program::current_mark = 0;

InstructionList Program::instructions;
Things Program::static_data;
InternalTypeList Program::internal_types;
InternalTypeMap Program::internal_type_map;
UserTypeList Program::user_types;
Index Program::entry = static_cast<Index>(-1);
Index Program::initial_frame_size = static_cast<Index>(-1);
SourceMap Program::source_map;
Source Program::source;


Thing Program::pop() {
    /**
     * Pop an item from the program stack and return it
     */
    if(stack.empty())
        critical_abort(EMPTY_PROGRAM_STACK);

    auto ti = stack.front();
    stack.pop_front();
    return ti;
}

void Program::load(ProgramInfo &info) {
    /**
     * Prepares bytecode for execution
     */
    entry = info.entry_point;
    initial_frame_size = info.root_stack_frame_size;
    static_data = info.static_data;
    instructions = info.instructions;
    source_map = info.source_map;
    source = info.program_source;
    internal_types = info.imported_types;
    user_types = info.user_types;

    Index index = 0;
    for(InternalType internal_type : internal_types){ // Used to look up exception types
        internal_type_map[internal_type] = index++;
    }
}


void Program::status(Index counter, const Instruction& instruction) {
    /**
     * Prints diagnostic information about the currently executing instruction
     */
    auto source_idx = source_map[instruction.index];



    std::cerr << "[" << counter << "] Executing instruction " << describe(instruction.opcode) << ": " << instruction.target << ", "
              << instruction.secondary << " -> [";
    std::for_each(Program::stack.begin(), Program::stack.end(),
                  [](const Thing &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });
    std::cerr << "] -> [";
    if(!Program::frames.empty())
        std::for_each(Program::frame().begin(), Program::frame().end(),
                      [](const Thing &thing) { std::cerr << (thing ? thing->text() : "?") << ","; });

    if(source_idx >= source.size())
        throw RuntimeError("Invalid source reference");

    std::cerr << "] -> [" << trim(source[source_idx]) << "]" << std::endl;

}

void inline Program::copy_args(Size count){
    /**
     * Copy arguments from the stack into the current frame
     */
    for (size_t i = 0; i < count; i++) {
        Program::frame()[count - i] = Program::pop();
    }
}

void Program::execute() {
    /**
     * The primary execution loop
     */

    auto counter_end = instructions.size();

    std::stack<Index> return_stack;
    std::stack<Index> call_stack;

    return_stack.push(counter_end);
    call_stack.push(entry);

    Program::create_frame(initial_frame_size);
    Instruction instruction(static_cast<Index>(-1), Opcode::INVALID);

    std::cerr << "Starting execution (upper boundary " << counter_end << ")" << std::endl;
    for (Index counter = entry; counter < counter_end;) {
        handle_instruction:

        instruction = instructions[counter];

        Program::status(counter, instruction);

        switch (instruction.opcode) {

            case Opcode::PASS:
                break;

            case Opcode::CALL: {
                return_stack.push(counter + 1);
                counter = instruction.target;

                call_stack.push(instruction.target);
                Program::create_frame(instruction.secondary);

                goto handle_instruction;
            }

            case Opcode::CALL_VIRTUAL: {
                auto method = user_types[instruction.target].method(instruction.secondary);

                return_stack.push(counter + 1);
                counter = method.address;

                call_stack.push(counter);
                Program::create_frame(method.frame_size);

                goto handle_instruction;
            }


            case Opcode::CALL_INTERNAL: {
                try {
                    Program::internal_types[instruction.target]->call(instruction.secondary);
                    break;
                } catch(Thing exc){
                    Program::push(exc);
                    counter = Program::exception(counter, internal_type_map[exc->type()], call_stack, return_stack);
                    goto handle_instruction;
                }
            }

            case Opcode::INSTANTIATE: {
                auto new_thing = Program::create<ThingInstance>(instruction.secondary);
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

            case Opcode::ASSIGN_LOCAL: {
                Program::frame()[instruction.target] = Program::frame()[instruction.secondary];
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
                gc_cycle();
                continue; // Not goto handle_instruction because this may be the program end
            }

            case Opcode::THROW: {
                counter = Program::exception(counter, instruction.target, call_stack, return_stack);
                goto handle_instruction;
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


void Program::gc_cycle() {
    /**
     * Full mark-sweep GC cycle
     */

    Program::mark();
    Program::sweep();
}



void Program::mark() {
    /**
     * Marks all object roots by scanning all stack frames and the program stack
     */

    current_mark++;

    for(auto& frame : frames){
        for(auto& elem : frame) {
            mark(elem);
        }
    }

    for(auto& elem : stack){
        mark(elem);
    }
}

void Program::mark(const Thing &thing) {
    /**
     * Mark an object and recursively descend into its children
     */

    if(!thing || thing->color == current_mark)
        return;

    thing->color = current_mark;
    for(auto& child : thing->children())
        mark(child);
}

void Program::sweep() {
    /**
     * Collect all unreferenced objects (pending deletion), finalizes them and dealloactes their memory
     */

    ThingForwardList pending_deletion;

    for (auto it = objects.begin(), previous = objects.before_begin(); it != objects.end(); ) {
        if((*it)->color == current_mark){
            it++;
            previous++;
        } else {
            pending_deletion.push_front(*it);
            it = objects.erase_after(previous);
        }
    }

    for(auto item : pending_deletion){
        delete item;
    }

}


void Program::push(const Thing &instance) {
    /**
     * Push an item into the program stack
     */
    stack.push_front(instance);
}

void Program::push(int64_t value) {
    stack.push_front(Program::create<NumberInstance>(value));
}


void Program::push(bool value) {
    /**
     * Push an boolean value into the program stack
     */
    stack.push_front(value ? BOOL_TRUE : BOOL_FALSE);
}


Thing Program::data(Index index) {
    /**
     * Returns a reference to statically allocated data
     */
    return static_data[index];
}

void Program::create_frame(Size size) {
    /**
     * Creates a new stack frame
     */
    frames.push_front(Frame(size));
}

void Program::pop_frame() {
    /**
     * Pops the current stack frame
     */
    frames.pop_front();
}

Frame &Program::frame() {
    /**
     * Returns the current stack frame
     */
    return frames.front();
}

Thing Program::intern(Thing instance) {
    objects.push_front(instance);
    return instance;
}

Index Program::exception(Index counter, Index exception_type, std::stack<Index> &call_stack, std::stack<Index> &return_stack) {
    while(!call_stack.empty()){

        // Look for an exception handler which matches the exception we are throwing.
        for(Index i = call_stack.top() - 1; instructions[i].opcode != Opcode::SENTINEL_METHOD_DEFINITION; i -= 2){
            auto range = instructions[i], definition = instructions[i - 1];

            if(definition.secondary == exception_type && counter >= range.target && counter <= range.secondary){
                gc_cycle();
                return definition.target; // Return the jump target
            }
        }

        // If we couldn't find any, walk up the call stack
        counter = return_stack.top() - 1;

        Program::pop_frame();
        call_stack.pop();
        return_stack.pop();

    }

    critical_abort(UNHANDLED_EXCEPTION); // TODO: Obviously, we don't want a critical abort here
}
