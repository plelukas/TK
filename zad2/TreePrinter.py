
import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    '''@addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)
        '''

    @addToClass(AST.Node)
    def printTree(self):
        return ""


    @addToClass(AST.BinExpr)
    def printTree(self, level=0):
        ret = ""
        ret += (self.op.printTree(level+1) if isinstance(self.op, AST.Node) else "|" * level + str(self.op)) + "\n"
        ret += (self.left.printTree(level+1) if isinstance(self.left, AST.Node) else "|" * level + str(self.left)) + "\n"
        ret += (self.right.printTree(level+1) if isinstance(self.right, AST.Node) else "|" * level + str(self.right)) + "\n"
        return ret

    @addToClass(AST.Const)
    def printTree(self, level=0):
        ret = ""
        ret += (self.value.printTree(level+1) if isinstance(self.value, AST.Node) else "|" * level + str(self.value)) + "\n"
        return ret

    @addToClass(AST.Program)
    def printTree(self, level=0):
        ret = ""
        for i in self.declarations:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        for i in self.fundefs:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        for i in self.instructions:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.Inits)
    def printTree(self, level=0):
        ret = ""
        for i in range(0, level):
            ret += '|'
        ret += self.inits.printTree(level+1) + '\n'
        return ret

    @addToClass(AST.Init)
    def printTree(self, level=0):
        ret = ""
        ret += (self.id.printTree(level+1) if isinstance(self.id, AST.Node) else "|" * level + str(self.id)) + "\n"
        ret += (self.expression.printTree(level+1) if isinstance(self.expression, AST.Node) else "|" * level + str(self.expression))
        return ret

    @addToClass(AST.Instructions)
    def printTree(self, level=0):
        ret = ""
        for i in self.instructions:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + '\n'
        return ret

    @addToClass(AST.PrintInstruction)
    def printTree(self, level=0):
        ret = ""
        for i in self.expressions:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.LabeledInstruction)
    def printTree(self, level=0):
        ret = ""
        ret += (self.id.printTree(level+1) if isinstance(self.id, AST.Node) else "|" * level + str(self.id)) + "\n"
        ret += (self.instruction.printTree(level+1) if isinstance(self.instruction, AST.Node) else "|" * level + str(self.instruction)) + "\n"
        return ret

    @addToClass(AST.AssignmentInstruction)
    def printTree(self, level=0):
        ret = ""
        ret += (self.id.printTree(level+1) if isinstance(self.id, AST.Node) else "|" * level + str(self.id)) + "\n"
        ret += (self.expression.printTree(level+1) if isinstance(self.expression, AST.Node) else "|" * level + str(self.expression)) + "\n"
        return ret

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, level=0):
        ret = ""
        ret += (self.condition.printTree(level+1) if isinstance(self.condition, AST.Node) else "|" * level + str(self.condition)) + "\n"
        ret += (self.instruction.printTree(level+1) if isinstance(self.instruction, AST.Node) else "|" * level + str(self.instruction)) + "\n"
        ret += (self.instruction2.printTree(level+1) if isinstance(self.instruction2, AST.Node) else "|" * level + str(self.instruction2)) + '\n'
        return ret

    @addToClass(AST.WhileInstruction)
    def printTree(self, level=0):
        ret = ""
        ret += (self.condition.printTree(level+1) if isinstance(self.condition, AST.Node) else "|" * level + str(self.condition)) + "\n"
        ret += (self.instruction.printTree(level+1) if isinstance(self.instruction, AST.Node) else "|" * level + str(self.instruction)) + "\n"
        return ret

    @addToClass(AST.RepeatInstruction)
    def printTree(self, level=0):
        ret = ""
        for i in self.instructions:
            ret += i.printTree(level+1)
        ret += (self.condition.printTree(level+1) if isinstance(self.condition, AST.Node) else "|" * level + str(self.condition)) + "\n"
        return ret

    @addToClass(AST.ReturnInstruction)
    def printTree(self, level=0):
        ret = ""
        ret += "|" * level + self.expression.printTree(level+1) + "\n"
        return ret

    @addToClass(AST.CompoundInstuction)
    def printTree(self, level=0):
        ret = ""
        for i in self.declarations:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        for i in self.instructions:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.Expressions)
    def printTree(self, level=0):
        ret = ""
        for i in self.expressions:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.GroupedExpression)
    def printTree(self, level=0):
        ret = ""
        ret += (self.interior.printTree(level+1) if isinstance(self.interior, AST.Node) else "|" * level + str(self.interior)) + "\n"
        return ret

    @addToClass(AST.NamedExpression)
    def printTree(self, level=0):
        ret = ""
        ret += (self.id.printTree(level+1) if isinstance(self.id, AST.Node) else "|" * level + str(self.id)) + "\n"
        for i in self.expressions:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.NamedExpression)
    def printTree(self, level=0):
        ret = ""
        ret += (self.id.printTree(level+1) if isinstance(self.id, AST.Node) else "|" * level + str(self.id)) + "\n"
        for i in self.expressions:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.Fundefs)
    def printTree(self, level=0):
        ret = ""
        for i in self.fundefs:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.Fundef)
    def printTree(self, level=0):
        ret = ""
        ret += (self.id.printTree(level+1) if isinstance(self.id, AST.Node) else "|" * level + str(self.id)) + "\n"
        ret += (self.type.printTree(level+1) if isinstance(self.type, AST.Node) else "|" * level + str(self.type)) + "\n"
        for i in self.args:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        ret += (self.compound_instr.printTree(level+1) if isinstance(self.compound_instr, AST.Node) else "|" * level + str(self.compound_instr)) + "\n"
        return ret

    @addToClass(AST.Arguments)
    def printTree(self, level=0):
        ret = ""
        for i in self.args:
            ret += (i.printTree(level+1) if isinstance(i, AST.Node) else "|" * level + str(i)) + "\n"
        return ret

    @addToClass(AST.Fundef)
    def printTree(self, level=0):
        ret = ""
        ret += (self.id.printTree(level+1) if isinstance(self.id, AST.Node) else "|" * level + str(self.id)) + "\n"
        ret += (self.type.printTree(level+1) if isinstance(self.type, AST.Node) else "|" * level + str(self.type)) + "\n"
        return ret