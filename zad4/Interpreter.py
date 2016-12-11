
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)

operation_map = {
    '+': (lambda l, r: l + r),
    '-': (lambda l, r: l - r),
    '*': (lambda l, r: l * r),
    '/': (lambda l, r: l / r),
    '%': (lambda l, r: l % r),
    '<': (lambda l, r: l < r),
    '>': (lambda l, r: l > r),
    '<<': (lambda l, r: l << r),
    '>>': (lambda l, r: l >> r),
    '|': (lambda l, r: l | r),
    '&': (lambda l, r: l & r),
    '^': (lambda l, r: l ^ r),
    '<=': (lambda l, r: l <= r),
    '>=': (lambda l, r: l >= r),
    '==': (lambda l, r: l == r),
    '!=': (lambda l, r: l != r)
}


class Interpreter(object):

    def __init__(self):
        self.globalMemory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval
        return operation_map[node.op](r1, r2)

    # @when(AST.Const)
    # def visit(self, node):
    #     return node.value

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    # simplistic while loop interpretation
    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.RepeatInstruction)
    def visit(self, node):
        while True:
            try:
                node.instructions.accept(self)
                if node.condition.accept(self):
                    break
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.Variable)
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        pass

    @when(AST.Declarations)
    def visit(self, node):
        pass

    @when(AST.Declaration)
    def visit(self, node):
        pass

    @when(AST.Inits)
    def visit(self, node):
        pass

    @when(AST.Init)
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node):
        pass

    @when(AST.PrintInstruction)
    def visit(self, node):
        pass

    @when(AST.LabeledInstruction)
    def visit(self, node):
        pass

    @when(AST.AssignmentInstruction)
    def visit(self, node):
        pass

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        pass

    @when(AST.ReturnInstruction)
    def visit(self, node):
        pass

    @when(AST.ContinueInstruction)
    def visit(self, node):
        pass

    @when(AST.BreakInstruction)
    def visit(self, node):
        pass

    @when(AST.CompoundInstuction)
    def visit(self, node):
        pass

    @when(AST.Expressions)
    def visit(self, node):
        pass

    @when(AST.NamedExpression)
    def visit(self, node):
        pass

    @when(AST.Fundefs)
    def visit(self, node):
        pass

    @when(AST.Fundef)
    def visit(self, node):
        pass

    @when(AST.Arguments)
    def visit(self, node):
        pass

    @when(AST.Argument)
    def visit(self, node):
        pass

