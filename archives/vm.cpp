#include <cassert>
#include <stack>
#include <iostream>

enum OPCODES {
    STACK_INIT,
    PUSH_CONSTANT,
    PUSH,
    CALL,
    PRINT,
    RETURN,
    SET,
    BIN_ADD,
    BIN_MUL
};

struct Frame {
    int return_idx;
    int * data;
};

int main(){
    int program[][2] = {
            {STACK_INIT, 0},
            {PUSH_CONSTANT, 3},
            {PUSH_CONSTANT, 2},
            {CALL, 6},
            {PRINT, 0},
            {RETURN, 0},

            {STACK_INIT, 3},
            {SET, 0},
            {SET, 1},
            {PUSH, 0},
            {PUSH, 1},
            {BIN_ADD, 0},
            {PRINT, 0},
            {SET, 2},
            {PUSH, 2},
            {PUSH_CONSTANT, 2},
            {BIN_MUL, 0},
            {RETURN, 0}
    };

    int idx = 0;
    int return_idx = -1;
    int program_size = 100;


    std::stack<int> stack;
    std::stack<Frame> frames;
    Frame nf;
    frames.push(nf);

    while (idx != -1){
        assert(idx >= 0);

        OPCODES opcode = (OPCODES) program[idx][0];
        int arg = program[idx][1];

        int * frame = frames.top().data;
       // std::cout << "Index " << idx << std::endl;
        switch(opcode){
            case PUSH_CONSTANT:
                stack.push(arg);
                break;
            case SET:
                frame[arg] = stack.top();
                stack.pop();
                break;
            case PUSH:
                stack.push(frame[arg]);
                break;
            case BIN_ADD: {
                int lhs, rhs;
                lhs = stack.top();
                stack.pop();
                rhs = stack.top();
                stack.pop();
                stack.push(lhs + rhs);
                break;
            }
            case BIN_MUL: {
                int lhs, rhs;
                lhs = stack.top();
                stack.pop();
                rhs = stack.top();
                stack.pop();
                stack.push(lhs * rhs);
                break;
            }
            case RETURN:
                idx = frames.top().return_idx - 1;
                frames.pop();
                break;
            case CALL:
                return_idx = idx + 1;
                idx = arg - 1;
                break;
            case STACK_INIT: {
                Frame f = {return_idx, (int *) malloc(arg * sizeof(int *))};
                frames.push(f);
                break;
            }
            case PRINT:
                std::cout << "Head: " << stack.top() << std::endl;
                break;
        }

        idx += 1;



    }

}

