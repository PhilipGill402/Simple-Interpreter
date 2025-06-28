from NodeVisitor import *
from Lexer import *
from Parser import *

class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('integer'))
        self.define(BuiltinTypeSymbol('real'))

    def __str__(self) -> str:
        return f"Symbols: {[str(value) for value in self._symbols.values()]}" 

    def define(self, symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        return self._symbols.get(name)

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()
    
    def visitBlock(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compoundStatement)

    def visitProgram(self, node):
        self.visit(node.block)
    
    def visitBinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
    
    def visitNum(self, node):
        pass

    def visitUnaryOp(self, node):
        self.visit(node.expr)
    
    def visitCompound(self, node):
        for child in node.children:
            self.visit(child)
    
    def visitNoOp(self, node):
        pass

    def visitVarDecl(self, node):
        typeSymbol = self.symtab.lookup(node.typeNode.value)
        varName = node.varNode.value
        varSymbol = VarSymbol(varName, typeSymbol)
        self.symtab.define(varSymbol) 

    def visitAssign(self, node):
        varName = node.left.value
        varSymbol = self.symtab.lookup(varName)
        if varSymbol is None:
            raise NameError(str(varName))
    
    def visitVar(self, node):
        varName = node.value
        varSymbol = self.symtab.lookup(varName)
        if varSymbol is None:
            raise(NameError(str(varName)))


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)
    
    def __str__(self):
        return self.name
    
class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)
    
    def __str__(self) -> str:
        return f"<{self.name}:{self.type}>"
    
if __name__ == "__main__":
    text = """
    Program Part11;
    var
        x : INTEGER;
        y : REAL;
    
    begin

    end.
""" 
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtabBuilder = SymbolTableBuilder()
    symtabBuilder.visit(tree) 

    print(symtabBuilder.symtab) 
    