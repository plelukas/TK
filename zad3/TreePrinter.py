
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)


    '''@addToClass(AST.Node)
    def printTree(self, level=0):
        return "|" * level'''


    @addToClass(AST.BinExpr)
    def printTree(self, level=0):
        ret = ""
        ret += "|" * level + str(self.op) + '\n'
        ret += (self.left.printTree(level+1) if isinstance(self.left, AST.Node) else "|" * level + str(self.left))
        ret += (self.right.printTree(level+1) if isinstance(self.right, AST.Node) else "|" * level + str(self.right))
        return ret

    @addToClass(AST.Const)
    def printTree(self, level=0):
        ret = ""
        ret += "|" * level + str(self.value) + "\n"
        return ret

    @addToClass(AST.Program)
    def printTree(self, level=0):
        ret = ""
        ret += (self.declarations.printTree(level) if self.declarations is not None else "")
        ret += (self.fundefs.printTree(level) if self.fundefs is not None else "")
        ret += (self.instructions.printTree(level+1) if self.instructions is not None else "")
        return ret

    @addToClass(AST.Declarations)
    def printTree(self, level=0):
        ret = "|" * level + "DECLARATIONS" + '\n'
        for i in self.declarations:
            ret += i.printTree(level+1)
        return ret

    @addToClass(AST.Declaration)
    def printTree(self, level=0):
        ret = ""
        ret += self.inits.printTree(level)
        return ret

    @addToClass(AST.Inits)
    def printTree(self, level=0):
        ret = ""
        for i in self.inits:
            ret += i.printTree(level)
        return ret

    @addToClass(AST.Init)
    def printTree(self, level=0):
        ret = "|" * level + "=" + "\n"
        ret += "|" * (level+1) + str(self.id) +"\n"
        ret += self.expression.printTree(level+1)
        return ret

    @addToClass(AST.Instructions)
    def printTree(self, level=0):
        ret = ""
        for i in self.instructions:
            ret += i.printTree(level)
        return ret

    @addToClass(AST.PrintInstruction)
    def printTree(self, level=0):
        ret = ""
        ret += "|" * level + "PRINT" + "\n" + self.expressions.printTree(level+1)
        return ret

    @addToClass(AST.LabeledInstruction)
    def printTree(self, level=0):
        ret = "|" * level + "LABEL" + "\n"
        ret += "|" * (level+1) + str(self.id) + "\n"
        ret += self.instruction.printTree(level+1)
        return ret

    @addToClass(AST.AssignmentInstruction)
    def printTree(self, level=0):
        ret = "|" * level + "=" + "\n"
        ret += "|" * (level+1) + str(self.id) + "\n"
        ret += self.expression.printTree(level+1)
        return ret

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, level=0):
        ret = "|" * level + "IF" + "\n"
        ret += self.condition.printTree(level+1)
        ret += self.instruction.printTree(level+1)
        if self.instruction2:
            ret += "|" * level + "\n" + self.instruction2.printTree(level+1)
        return ret

    @addToClass(AST.WhileInstruction)
    def printTree(self, level=0):
        ret = "|" * level + "WHILE" + "\n"
        ret += self.condition.printTree(level+1)
        ret += self.instruction.printTree(level+1)
        return ret

    @addToClass(AST.RepeatInstruction)
    def printTree(self, level=0):
        ret = "|" * level + "REPEAT" + "\n"
        ret += self.instructions.printTree(level+1)
        ret += "|" * level + "UNTIL" + "\n"
        ret += self.condition.printTree(level+1)
        return ret

    @addToClass(AST.ReturnInstruction)
    def printTree(self, level=0):
        ret = "|" * level + "RETURN" + "\n"
        ret += self.expression.printTree(level+1)
        return ret

    @addToClass(AST.ContinueInstruction)
    def printTree(self, level=0):
        return "|" * level + "CONTINUE"

    @addToClass(AST.BreakInstruction)
    def printTree(self, level=0):
        return "|" * level + "BREAK"

    @addToClass(AST.CompoundInstuction)
    def printTree(self, level=0):
        ret = ""
        if self.declarations is not None:
            ret += self.declarations.printTree(level+1)
        if self.instructions is not None:
            ret += self.instructions.printTree(level+1)
        return ret

    @addToClass(AST.Expressions)
    def printTree(self, level=0):
        ret = ""
        if self.expressions is not None:
            for i in self.expressions:
                ret += i.printTree(level+1)
        return ret

    @addToClass(AST.NamedExpression)
    def printTree(self, level=0):
        ret = ""
        ret += "|" * level + str(self.id) + "\n"
        if self.expressions is not None:
            ret += self.expressions.printTree(level+1)
        return ret

    @addToClass(AST.Fundefs)
    def printTree(self, level=0):
        ret = ""
        if self.fundefs is not None:
            for i in self.fundefs:
                ret += i.printTree(level)
        return ret

    @addToClass(AST.Fundef)
    def printTree(self, level=0):
        ret = "FUNDEF" + "\n"
        ret += "|" * (level+1) + str(self.id) + "\n"
        ret += "|" * (level+1) + str(self.type) + "\n"
        ret += self.args.printTree(level+1)
        ret += self.compound_instr.printTree(level)
        return ret

    @addToClass(AST.Arguments)
    def printTree(self, level=0):
        ret = ""
        if self.args is not None:
            for i in self.args:
                ret += i.printTree(level)
        return ret

    @addToClass(AST.Argument)
    def printTree(self, level=0):
        ret = "|" * level + "ARGUMENT" + " " + str(self.id) + "\n"
        return ret
