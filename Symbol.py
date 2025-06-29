from __future__ import annotations
from NodeVisitor import *
from Lexer import *
from Parser import *
from AST import *

class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('integer'))
        self.define(BuiltinTypeSymbol('real'))

    def __str__(self) -> str:
        return f"Symbols: {[str(value) for value in self._symbols.values()]}" 

    def define(self, symbol: Symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        return self._symbols.get(name)

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()
    
    def visitBlock(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compoundStatement)

    def visitProgram(self, node: Program):
        self.visit(node.block)
    
    def visitBinOp(self, node: BinOp):
        self.visit(node.left)
        self.visit(node.right)
    
    def visitNum(self, node):
        pass

    def visitUnaryOp(self, node: UnaryOp):
        self.visit(node.expr)
    
    def visitCompound(self, node: Compound):
        for child in node.children:
            self.visit(child)
    
    def visitNoOp(self, node: NoOp):
        pass

    def visitVarDecl(self, node: VarDecl):
        typeSymbol = self.symtab.lookup(node.typeNode.value)
        if typeSymbol is None:
            raise NameError(f"Type '{node.typeNode.value}' not found in symbol table")
        varName = node.varNode.value
        varSymbol = VarSymbol(varName, typeSymbol)
        self.symtab.define(varSymbol) 

    def visitAssign(self, node: Assign):
        varName = node.left.value
        varSymbol = self.symtab.lookup(varName)
        if varSymbol is None:
            raise NameError(str(varName))
    
    def visitVar(self, node: Var):
        varName = node.value
        varSymbol = self.symtab.lookup(varName)
        if varSymbol is None:
            raise(NameError(str(varName)))


class Symbol(object):
    def __init__(self, name: str, type=None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)
    
    def __str__(self):
        return self.name
    
class VarSymbol(Symbol):
    def __init__(self, name: str, type: Symbol):
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
    