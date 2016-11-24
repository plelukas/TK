#!/usr/bin/python


class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)

    def __init__(self):
        self.children = ()


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.line = line
        self.op = op
        self.left = left
        self.right = right


class Const(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line


class Program(Node):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


class Declarations(Node):
    def __init__(self):
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class Inits(Node):
    def __init__(self):
        self.inits = []

    def addInit(self, init):
        self.inits.append(init)

class Init(Node):
    def __init__(self, id, expression, line):
        self.id = id
        self.expression = expression
        self.line = line

class Instructions(Node):
    def __init__(self):
        self.instructions = []

    def addInstruction(self, instruction):
        self.instructions.append(instruction)


class PrintInstruction(Node):
    def __init__(self, expressions, line):
        self.expressions = expressions
        self.line = line


class LabeledInstruction(Node):
    def __init__(self, id, instruction, line):
        self.id = id
        self.instruction = instruction
        self.line = line


class AssignmentInstruction(Node):
    def __init__(self, id, expression, line):
        self.id = id
        self.expression = expression
        self.line = line


class ChoiceInstruction(Node):
    def __init__(self, condition, instruction, instruction2=None):
        self.condition = condition
        self.instruction = instruction
        self.instruction2 = instruction2


class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition


class ReturnInstruction(Node):
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line


class ContinueInstruction(Node):
    pass

class BreakInstruction(Node):
    pass

class CompoundInstuction(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions

class Expressions(Node):
    def __init__(self):
        self.expressions = []

    def addExpression(self, expr):
        self.expressions.append(expr)

class GroupedExpression(Node):
    def __init__(self, interior):
        self.interior = interior

class NamedExpression(Node):
    # wywolanie funkcji
    def __init__(self, id, expressions, line):
        self.id = id
        self.expressions = expressions
        self.line = line


class Fundefs(Node):
    def __init__(self):
        self.fundefs = []

    def addFundef(self, fundef):
        self.fundefs.append(fundef)

class Fundef(Node):
    # type is return type
    def __init__(self, type, id, args, compound_instr):
        self.id = id
        self.type = type
        self.args = args
        self.compound_instr = compound_instr

class Arguments(Node):
    def __init__(self):
        self.args = []

    def addArgument(self, arg):
        self.args.append(arg)

class Argument(Node):
    def __init__(self, type, id, line):
        self.type = type
        self.id = id
        self.line = line


