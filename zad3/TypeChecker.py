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
        self.loop_flag = False
        self.uniq_arg = 0

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        line = node.line

        if type1 is None or type2 is None:
            return None

        if ttype[op][type1][type2] is None:
            print("Error: Illegal operation, {} {} {}: line {}".format(type1, op, type2, line))
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
            print("Error: Usage of undeclared variable '{}': line {}".format(name, line))
        elif isinstance(symbol, FunctionSymbol):
            print("Error: Function identifier '{}' used as a variable: line {}".format(name, line))
        else:
            return symbol.type

    def visit_Program(self, node):
        if node.declarations is not None:
            self.visit(node.declarations)
        if node.fundefs is not None:
            self.visit(node.fundefs)
        if node.instructions is not None:
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
            print("Error: Variable '{}' already declared: line {}".format(node.id, node.line))
        except KeyError:
            symbol = self.table.getGlobal(node.id)
            if isinstance(symbol, FunctionSymbol):
                print("Error: Function identifier '{}' used as a variable: line {}".format(node.id, line))
                return

            id = node.id
            type = self.visit(expr)

            if self.presentType != type and not (self.presentType == 'float' and type == 'int'):
                if self.presentType == 'int' and type == 'float':
                    print("WARNING: possible loss of precision at line " + str(line))
                    self.table.put(id, VariableSymbol(id, type))
                elif type is not None:
                    print("Error: Assignment of {} to {}: line {}"
                          .format(type, self.presentType, line))
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

        expr_type = self.visit(expr)

        symbol = self.table.getGlobal(id)
        if symbol is None:
            print("Error: Variable '{}' undefined in current scope: line {}".format(id, line))
        else:
            symbol_type = symbol.type
            if symbol_type != expr_type and not (symbol_type == 'float' and expr_type == 'int'):
                if symbol_type == 'int' and expr_type == 'float':
                    print("WARNING: possible loss of precision at line " + str(line))
                elif expr_type is not None:
                    print("Error: Assignment of {} to {}: line {}"
                          .format(expr_type, symbol_type, line))


    def visit_ChoiceInstruction(self, node):
        condition = node.condition
        instruction = node.instruction
        instruction2 = node.instruction2

        self.visit(condition)
        self.visit(instruction)
        if instruction2 is not None:
            self.visit(instruction2)


    def visit_WhileInstruction(self, node):
        self.visit(node.condition)
        if not self.loop_flag:
            self.loop_flag = True
            self.visit(node.instruction)
            self.loop_flag = False
        else:
            self.visit(node.instruction)

    def visit_RepeatInstruction(self, node):
        if not self.loop_flag:
            self.loop_flag = True
            for i in node.instructions:
                self.visit(i)
            self.loop_flag = False
        else:
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
                elif expression_type is not None:
                    print("Error: Improper returned type, expected {}, got {}: line {}"
                          .format(fun.type, expression_type, node.line))
        else:
            print("Error: return instruction outside a function: line " + str(node.line))

    def visit_ContinueInstruction(self, node):
        if not self.loop_flag:
            print("Error: continue instruction outside a loop: line {}".format(node.line))

    def visit_BreakInstruction(self, node):
        if not self.loop_flag:
            print("Error: break instruction outside a loop: line {}".format(node.line))

    def visit_CompoundInstuction(self, node):
        if node.declarations is not None:
            self.visit(node.declarations)
        if node.instructions is not None:
            self.visit(node.instructions)

    def visit_Expressions(self, node):
        for i in node.expressions:
            self.visit(i)

    def visit_GroupedExpression(self, node):
        return self.visit(node.interior)

    def visit_NamedExpression(self, node):
        function = self.table.get(node.id)
        if function is None:
            print("Error: Call of undefined fun '{}': line {}".format(node.id, node.line))
            return None
        else:
            if len(node.expressions.expressions) != len(function.arguments):
                print("Error: Improper number of args in {} call: line {}"
                      .format(function.name, node.line))
                return function.type
            for i in range(0, len(node.expressions.expressions)):
                current_type = self.visit(node.expressions.expressions[i])
                arg_type = function.arguments[i].type
                if current_type != arg_type and not (arg_type == 'float' and current_type == 'int'):
                    if current_type == 'float' and arg_type == 'int':
                        print("WARNING: possible loss of precision at line " + str(node.line))
                    else:
                        print("Error: Improper type of args in {} call: line {}"
                            .format(node.id, node.line))
            return function.type

    def visit_Fundefs(self, node):
        for i in node.fundefs:
            self.visit(i)

    def visit_Fundef(self, node):
        if self.table.getParentScope() is not None:
            print("ERROR: Function defined in non-global scope at line " + str(node.line))
        else:
            if self.table.get(node.id) is not None:
                print("Error: Redefinition of function '{}': line {}".format(node.id, node.line))
            else:
                self.presentFunction = FunctionSymbol(node.id, node.type, SymbolTable(self.table, node.id))
                function = self.presentFunction
                self.table.put(node.id, self.presentFunction)
                self.table = self.presentFunction.table
                if node.args is not None:
                    self.visit(node.args)
                self.presentFunction.arguments = function.table.entries.values()
                self.visit(node.compound_instr)
                self.table = self.table.getParentScope()
                self.presentFunction = None

    def visit_Arguments(self, node):
        for i in node.args:
            self.visit(i)

    def visit_Argument(self, node):
        try:
            x = self.table.entries[node.id]
            print("Error: Variable '{}' already declared: line {}".format(node.id, node.line))
            self.table.put(self.uniq_arg, VariableSymbol(self.uniq_arg, node.type))
            self.uniq_arg += 1
        except KeyError:
            self.table.put(node.id, VariableSymbol(node.id, node.type))
