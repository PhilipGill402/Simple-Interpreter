from __future__ import annotations
from NodeVisitor import *
from Lexer import *
from Parser import *
from AST import *

class SymbolTable(object):
    def __init__(self) -> None:
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self) -> None:
        self.define(BuiltinTypeSymbol('integer'))
        self.define(BuiltinTypeSymbol('real'))

    def __str__(self) -> str:
        return f"Symbols: {[str(value) for value in self._symbols.values()]}" 

    def define(self, symbol: Symbol) -> None:
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Union[None, Symbol]:
        return self._symbols.get(name)

class SymbolTableBuilder(NodeVisitor):
    def __init__(self) -> None:
        self.symtab = SymbolTable()
    
    def visitBlock(self, node: Block) -> None:
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compoundStatement)

    def visitProgram(self, node: Program) -> None:
        self.visit(node.block)
    
    def visitBinOp(self, node: BinOp):
        self.visit(node.left)
        self.visit(node.right)
    
    def visitNum(self, node: Num) -> None:
        pass

    def visitUnaryOp(self, node: UnaryOp) -> None:
        self.visit(node.expr)
    
    def visitCompound(self, node: Compound) -> None:
        for child in node.children:
            self.visit(child)
    
    def visitNoOp(self, node: NoOp) -> None:
        pass

    def visitVarDecl(self, node: VarDecl) -> None:
        typeSymbol = self.symtab.lookup(node.typeNode.value)
        varName = node.varNode.value
        varSymbol = VarSymbol(varName, typeSymbol)

        if self.symtab.lookup(varName) is not None:
            raise Exception(f"Error: Duplicate identifier '{varName}' found") 
        self.symtab.define(varSymbol) 

    def visitAssign(self, node: Assign) -> None:
        self.visit(node.right)
        self.visit(node.left)
    
    def visitVar(self, node: Var) -> None:
        varName = node.value
        varSymbol = self.symtab.lookup(varName)
        if varSymbol is None:
            raise NameError(f"Error: Symbol(identifier) not found '{varName}'")

    def visitProcedureDecl(self, node: ProcedureDecl) -> None:
        pass


class Symbol(object):
    def __init__(self, name: str, type=None) -> None:
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def __str__(self) -> str:
        return self.name
    
class VarSymbol(Symbol):
    def __init__(self, name: str, type: Symbol) -> None:
        super().__init__(name, type)
    
    def __str__(self) -> str:
        return f"<{self.name}:{self.type}>"
    
if __name__ == "__main__":
    text = """
    program Main;
   var x  : integer;

begin
    x := y;
end.
""" 
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtabBuilder = SymbolTableBuilder()
    symtabBuilder.visit(tree) 

    print(symtabBuilder.symtab) 
    