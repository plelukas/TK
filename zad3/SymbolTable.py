#!/usr/bin/python


class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class VariableSymbol(Symbol):
    pass

class FunctionSymbol(Symbol):
    def __init__(self, name, type, table):
        self.name = name
        self.type = type
        self.table = table
        self.arguments = []


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.entries = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.entries[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        ret = self.entries.get(name)
        if ret is None:
            if self.parent is None:
                return None
            else:
                ret = self.parent.get(name)
        return ret

    def getGlobal(self, name):
        return self.entries.get(name) or (None if self.parent is None else self.parent.getGlobal(name))

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        pass
    #

    def popScope(self):
        pass
    #

