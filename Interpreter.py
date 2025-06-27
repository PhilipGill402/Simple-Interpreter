from NodeVisitor import *
from Constants import *
from AST import *

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}
    
    def visitBinOp(self, node: BinOp):
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
        
    def visitNum(self, node: Num):
        return node.value

    def visitUnaryOp(self, node: UnaryOp):
        if node.op.type == PLUS:
            return +self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr) 
    
    def visitCompound(self, node: Compound):
        for child in node.children:
            self.visit(child) 

    def visitAssign(self, node: Assign):
        varName = node.left.value
        self.GLOBAL_SCOPE[varName] = self.visit(node.right) 

    def visitVar(self, node: Var):
        varName = node.value
        value = self.GLOBAL_SCOPE.get(varName)

        if value is None:
            raise NameError(repr(varName))
        else:
            return value 

    def visitNoOp(self, node: NoOp):
        pass

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)