from thinglang.compiler import CompilationContext
from thinglang.compiler.opcodes import OpcodeCallInternal
from thinglang.foundation import Foundation
from thinglang.lexer.lexical_definitions import REVERSE_OPERATORS
from thinglang.lexer.tokens.arithmetic import LexicalAddition, LexicalMultiplication, LexicalSubtraction, \
    LexicalDivision
from thinglang.lexer.tokens.logic import LexicalEquality, LexicalInequality, LexicalGreaterThan, LexicalLessThan
from thinglang.parser.nodes import BaseNode
from thinglang.utils.type_descriptors import ValueType, ReplaceableArguments


class ArithmeticOperation(BaseNode, ValueType, ReplaceableArguments):
    OPERATIONS = {
        LexicalAddition: lambda lhs, rhs: lhs + rhs,
        LexicalMultiplication: lambda lhs, rhs: lhs * rhs,
        LexicalSubtraction: lambda lhs, rhs: lhs - rhs,
        LexicalDivision: lambda lhs, rhs: lhs / rhs,
        LexicalEquality: lambda lhs, rhs: lhs == rhs,
        LexicalInequality: lambda lhs, rhs: lhs != rhs,
        LexicalGreaterThan: lambda lhs, rhs: lhs > rhs,
        LexicalLessThan: lambda lhs, rhs: lhs < rhs
    }

    def __init__(self, slice):
        super(ArithmeticOperation, self).__init__(slice)
        self.arguments = [slice[0], slice[2]]
        self.operator = type(slice[1])

    def evaluate(self, resolver):
        return self.OPERATIONS[self.operator](self[0].evaluate(resolver), self[1].evaluate(resolver))

    def describe(self):
        return '|{} {} {}|'.format(self[0], self.operator, self[1])

    def __getitem__(self, item):
        return self.arguments[item]

    def references(self):
        return self.arguments

    def transpile(self):
        return '{} {} {}'.format(self.arguments[0].transpile(), REVERSE_OPERATORS[self.operator], self.arguments[1].transpile())

    def compile(self, context: CompilationContext, captured=False): # TODO: duplicate of actual call
        context.push_ref(self.arguments[1])
        context.push_ref(self.arguments[0])
        type_id = self.arguments[0].type_id()
        context.append(OpcodeCallInternal(Foundation().INTERNAL_TYPE_ORDERING[type_id], Foundation().type(type_id).index(self.operator.transpile())))
        if self.parent is not None and not captured:
            context.append(BytecodeSymbols.pop())  # TODO: Dead branch?

    def type_id(self):
        assert all(x.type_id() == self.arguments[0].type_id() for x in self.arguments)
        return self.arguments[0].type_id()
