#!/usr/bin/python
import re

from scanner import Scanner
import AST


class Cparser(object):

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens
    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    
    
    def p_program(self, p):
        """program : declarations fundefs_opt instructions_opt"""
        p[0] = AST.Program(
            None if len(p[1].declarations) == 0 else p[1],
            None if len(p[2].fundefs) == 0 else p[2],
            None if len(p[3].instructions) == 0 else p[3]
        )
        #print(p[0])


    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) == 3:
            p[0] = p[1]
            p[0].addDeclaration(p[2])
        else:
            p[0] = AST.Declarations()
                     
    
    def p_declaration(self, p):
        """declaration : TYPE inits ';' 
                       | error ';' """
        if len(p) == 4:
            p[0] = AST.Declaration(p[1], p[2])


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[0] = p[1]
            p[0].addInit(p[3])
        else:
            p[0] = AST.Inits()
            p[0].addInit(p[1])


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = AST.Init(p[1], p[3], p.lineno(1))
 

    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.Instructions()

    
    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[0] = p[1]
            p[0].addInstruction(p[2])
        else:
            p[0] = AST.Instructions()
            p[0].addInstruction(p[1])
    
    
    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr 
                       | repeat_instr 
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]
    
    
    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        p[0] = AST.PrintInstruction(p[2], p.lineno(1))

    
    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstruction(p[1], p[3], p.lineno(1))
    
    
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.AssignmentInstruction(p[1], p[3], p.lineno(1))
    
    
    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        if len(p) < 8:
            p[0] = AST.ChoiceInstruction(p[3], p[5])
        else:
            p[0] = AST.ChoiceInstruction(p[3], p[5], p[7])
    
    
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstruction(p[3], p[5])


    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstruction(p[2], p[4])

    
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstruction(p[2], p.lineno(1))

    
    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstruction()

    
    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstruction()
    
    
    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        p[0] = AST.CompoundInstuction(None if len(p[2].declarations) == 0 else p[2], None if len(p[3].instructions) == 0 else p[3])

    
    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]


    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        if re.match(r"\d+(\.\d*)|\.\d+", p[1]):
            p[0] = AST.Float(p.lineno(1), p[1])
        elif re.match(r"\d+", p[1]):
            p[0] = AST.Integer(p.lineno(1), p[1])
        else:
            p[0] = AST.String(p.lineno(1), p[1])
    
    
    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        if len(p) == 2:
            if isinstance(p[1], AST.Const):
                p[0] = p[1]
            else:
                p[0] = AST.Variable(p[1], p.lineno(1))
        elif len(p) == 4:
            if p[1] == "(":
                p[0] = AST.GroupedExpression(p[2])
            else:
                p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))
        else:
            # len = 5
            p[0] = AST.NamedExpression(p[1], p[3], p.lineno(1))
    
    
    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        p[0] = None if len(p) == 1 else p[1]

    
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[0] = p[1]
            p[0].addExpression(p[3])
        else:
            p[0] = AST.Expressions()
            p[0].addExpression(p[1])
    
    
    def p_fundefs_opt(self, p):
        """fundefs_opt : fundefs
                       | """
        p[0] = AST.Fundefs() if len(p) == 1 else p[1]


    def p_fundefs(self, p):
        """fundefs : fundefs fundef
                   | fundef """
        if len(p) == 3:
            p[0] = p[1]
            p[0].addFundef(p[2])
        else:
            p[0] = AST.Fundefs()
            p[0].addFundef(p[1])

          
    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.Fundef(p[1], p[2], p[4], p[6])
    
    
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        p[0] = None if len(p) == 1 else p[1]


    def p_args_list(self, p):
        """args_list : args_list ',' arg 
                     | arg """
        if len(p) == 4:
            p[0] = p[1]
            p[0].addArgument(p[3])
        else:
            p[0] = AST.Arguments()
            p[0].addArgument(p[1])


    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Argument(p[1], p[2], p.lineno(1))

    