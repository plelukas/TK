
import ply.lex as lex
import ply.yacc as yacc
import ast


tokens = ('TYPE', )


tree = ast.parse("x+y*z")
ast.dump(tree)
Module(body=[Expr(value=BinOp(left=Name(id='x', ctx=Load()), op=Add(),
                              right=BinOp(left=Name(id='y', ctx=Load()), op=Mult(), right=Name(id='z', ctx=Load()))))])
