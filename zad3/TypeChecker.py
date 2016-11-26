#!/usr/bin/python

import AST

from collections import defaultdict

from SymbolTable import SymbolTable, VariableSymbol, FunctionSymbol

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
        self.presentFunction = None

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
        id = None
        expr = node.expression
        line = node.line

        try:
            id = self.table.entries[node.id]
            print("{} already defined".format(node.id))
        except KeyError:
            id = node.id
            type = self.visit(expr)
            if self.presentType != type and not (self.presentType == 'float' and type == 'int'):
                if self.presentType != 'int' or type != 'float':
                    print("ERROR: Type mismatch in {} at line {}. Expected {}, got {}"
                          .format(id, line, self.presentType, type))
                else:
                    print("WARNING: possible loss of precision at line " + str(line))
                    self.table.put(id, VariableSymbol(id, type))
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
            symbol_type = symbol.type
            expr_type = self.visit(expr)
            if symbol_type != expr_type and not (symbol_type == 'float' and expr_type == 'int'):
                if symbol_type == 'int' and expr_type == 'float':
                    print("WARNING: possible loss of precision at line " + str(line))
                else:
                    print("ERROR: Type mismatch in {} at line {}. Expected {}, got {}."
                          .format(id, line, symbol_type, expr_type))


    def visit_ChoiceInstruction(self, node):
        condition = node.condition
        instruction = node.instruction
        instruction2 = node.instruction2

        self.visit(condition)
        self.visit(instruction)
        if instruction2 is not None:
            self.visit(instruction2)


    def visit_WhileInstruction(self, node):
        if self.presentFunction is None:
            print("ERROR: While statement out of function")
        else:
            self.visit(node.condition)
            self.visit(node.instruction)

    def visit_RepeatInstruction(self, node):
        for i in node.instructions:
            self.visit(i)
        self.visit(node.condition)

    def visit_ReturnInstruction(self, node):
        expression_type = self.visit(node.expression)
        fun = self.presentFunction
        if isinstance(fun, FunctionSymbol):
            if expression_type != fun.type and not(fun.type == 'float' and expression_type == 'int'):
                if fun.type == 'int' and expression_type == 'float':
                    print("WARNING: possible loss of precision at line " + str(node.line))
                else:
                    print("ERROR at line {}: returned type {}, got {}."
                          .format(node.line, fun.type, expression_type))
        else:
            print("Return statement outside function at line " + str(node.line))

    def visit_ContinueInstruction(self, node):
        if self.presentFunction is None:
            print ("ERROR: Continue statement out of function")

    def visit_BreakInstruction(self, node):
        if self.presentFunction is None:
            print ("ERROR: Continue statement out of function")

    def visit_CompoundInstuction(self, node):
        new_table = SymbolTable(self.table, "new_scope")
        self.table = new_table
        if node.declarations is not None:
            self.visit(node.declarations)
        if node.instructions is not None:
            self.visit(node.instructions)
        self.table = self.table.getParentScope()

    def visit_Expressions(self, node):
        for i in node.expressions:
            self.visit(i)

    def visit_GroupedExpression(self, node):
        return self.visit(node.interior)

    def visit_NamedExpression(self, node):
        function = self.table.get(node.id)
        if function is None:
            print("ERROR: Function " + str(node.id) + " not defined, line " + str(node.line))
            return None
        else:
            if len(node.expressions.expressions) != len(function.arguments):
                print("Function {} needs {} arguments, but {} are provided"
                      .format(function.id, len(function.arguments), len(node.expressions.expressions)))
                return function.type
            for i in range(0, len(node.expressions.expressions)):
                current_type = self.visit(node.expressions.expressions[i])
                arg_type = function.arguments[i].type
                if current_type != arg_type and not (arg_type == 'float' and current_type == 'int'):
                    if current_type == 'float' and arg_type == 'int':
                        print("WARNING: possible loss of precision at line " + str(node.line))
                    else:
                        print("ERROR: Type mismatch at line {}. Expected {}, got {}."
                            .format(node.line, arg_type, current_type))
            return function.type

    def visit_Fundefs(self, node):
        for i in node.fundefs:
            self.visit(i)

    def visit_Fundef(self, node):
        if self.table.getParentScope() is not None:
            print("ERROR: Function defined in non-global scope at line " + str(node.line))
        else:
            if self.table.get(node.id) is not None:
                print("ERROR at line {}: Function {} already defined".format(node.line, node.id))
            else:
                self.presentFunction = FunctionSymbol(node.id, node.type, SymbolTable(self.table, node.id))
                function = self.presentFunction
                self.table.put(node.id, self.presentFunction)
                self.table = self.presentFunction.table
                if node.args is not None:
                    self.visit(node.args)
                self.presentFunction.arguments = [i for i in function.table.entries.values()]
                self.visit(node.compound_instr)
                self.table = self.table.getParentScope()
                self.presentFunction = None

    def visit_Arguments(self, node):
        for i in node.args:
            self.visit(i)

    def visit_Argument(self, node):
        try:
            x = self.table.entries[node.id]
            print("ERROR at line {}: Argument {} already defined".format(node.line, node.id))
        except KeyError:
            self.table.put(node.id, VariableSymbol(node.id, node.type))
