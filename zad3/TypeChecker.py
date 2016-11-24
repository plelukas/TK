#!/usr/bin/python

import AST

from collections import defaultdict

from SymbolTable import SymbolTable, VariableSymbol

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

                    # simpler version of generic_visit, not so general
                    # def generic_visit(self, node):
                    #    for child in node.children:
                    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.table = SymbolTable(None, 'global')
        self.presentType = None

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        line = node.line

        if ttype[op][type1][type2] is None:
            print("ERROR: Undefined operation {} for {} and {} at line {}.".format(op, type1, type2, line))
        return ttype[op][type1][type2]


    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        name = node.name
        line = node.line

        symbol = self.table.getGlobal(name)
        if symbol is None:
            print("ERROR: {} not defined at line {}.".format(name, line))
        else:
            return symbol.type

    def visit_Program(self, node):
        self.visit(node.declarations)
        self.visit(node.fundefs)
        self.visit(node.instructions)

    def visit_Declarations(self, node):
        for decl in node.declarations:
            self.visit(decl)

    def visit_Declaration(self, node):
        self.presentType = node.type
        self.visit(node.inits)
        self.presentType = None

    def visit_Inits(self, node):
        inits = node.inits
        for init in inits:
            self.visit(init)

    def visit_Init(self, node):
        id = node.id
        expr = node.expression
        line = node.line

        type = self.visit(expr)
        if self.presentType != type:
            print("ERROR: Type mismatch in {} at line {}.".format(id, line))
        else:
            self.table.put(id, VariableSymbol(id, type))

    def visit_Instructions(self, node):
        for instr in node.instructions:
            self.visit(instr)

    def visit_PrintInstruction(self, node):
        self.visit(node.expressions)

    def visit_LabeledInstruction(self, node):
        pass

    def visit_AssignmentInstruction(self, node):
        id = node.id
        expr = node.expression
        line = node.line

        symbol = self.table.getGlobal(id)
        if symbol is None:
            print("ERROR: {} not defined at line {}.".format(id, line))
        else:
            type = symbol.type
            if type != self.visit(expr):
                print("ERRORL Type mismatch in {} at line {}.".format(id, line))


    def visit_ChoiceInstruction(self, node):
        pass

    def visit_WhileInstruction(self, node):
        pass

    def visit_RepeatInstruction(self, node):
        pass

    def visit_ReturnInstruction(self, node):
        pass

    def visit_ContinueInstruction(self, node):
        pass

    def visit_BreakInstruction(self, node):
        pass

    def visit_CompoundInstuction(self, node):
        pass

    def visit_Expressions(self, node):
        pass

    def visit_GroupedExpression(self, node):
        pass

    def visit_NamedExpression(self, node):
        pass

    def visit_Fundefs(self, node):
        pass

    def visit_Fundef(self, node):
        pass

    def visit_Arguments(self, node):
        pass

    def visit_Argument(self, node):
        pass

