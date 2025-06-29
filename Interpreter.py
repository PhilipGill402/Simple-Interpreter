from NodeVisitor import *
from Constants import *
from AST import *
from Parser import Parser 

class Interpreter(NodeVisitor):
    def __init__(self, parser: Parser) -> None:
        self.parser = parser
        self.GLOBAL_SCOPE = {}
    
    def visitBinOp(self, node: BinOp) -> Union[None, int]:
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)

        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        
        elif node.op.type == INTDIV:
            return self.visit(node.left) // self.visit(node.right)
        
    def visitNum(self, node: Num) -> int:
        return node.value

    def visitUnaryOp(self, node: UnaryOp) -> Union[None, int]:
        if node.op.type == PLUS:
            return +self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr) 
    
    def visitCompound(self, node: Compound) -> None:
        for child in node.children:
            self.visit(child) 

    def visitAssign(self, node: Assign) -> None:
        varName = node.left.value
        self.GLOBAL_SCOPE[varName] = self.visit(node.right) 

    def visitVar(self, node: Var) -> int:
        varName = node.value
        value = self.GLOBAL_SCOPE.get(varName)

        if value is None:
            raise NameError(repr(varName))
        else:
            return value 
    
    def visitProgram(self, node: Program) -> None:
        self.visit(node.block)
    
    def visitBlock(self, node: Block) -> None:
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compoundStatement)

    def visitVarDecl(self, node: VarDecl) -> None:
        pass

    def visitType(self, node: Type) -> None:
        pass

    def visitNoOp(self, node: NoOp) -> None:
        pass

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)