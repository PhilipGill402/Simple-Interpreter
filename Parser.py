from Token import *
from Constants import *
from Lexer import *
from AST import *
from Interpreter import *
from collections import deque

class Parser(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer 
        self.currentToken = self.lexer.getNextToken() 
    
    def error(self):
        raise Exception("Error parsing input")

    def eat(self, tokenType):
        if self.currentToken.type == tokenType:
            self.currentToken = self.lexer.getNextToken()
        else:
            self.error()

    def program(self):
        node = self.compoundStatement() 
        self.eat(DOT)

        return node

    def compoundStatement(self):
        self.eat(BEGIN)
        nodes = self.statementList()
        self.eat(END) 

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root 

    def statementList(self):
        node = self.statement()
        results = [node]

        while self.currentToken.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        
        if self.currentToken.type == ID:
            self.error()
        
        return results

    def statement(self):
        if self.currentToken.type == BEGIN:
            return self.compoundStatement() 
        elif self.currentToken.type == ID:
            return self.assignmentStatement()
        else:
            node = self.empty()

        return node

    def assignmentStatement(self):
        left = self.variable()
        token = self.currentToken
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)

        return node

    def variable(self):
        node = Var(self.currentToken)
        self.eat(ID)

        return node 

    def empty(self):
        return NoOp()

    def factor(self):
        token = self.currentToken

        if token.type == INTEGER:
            self.eat(INTEGER)
            
            return Num(token) 
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            
            return node 
        elif token.type == PLUS:
                self.eat(PLUS)
                node = UnaryOp(token, self.factor())

                return node 
        elif token.type == MINUS:
                self.eat(MINUS)
                node = UnaryOp(token, self.factor())

                return node 
        else:
            node = self.variable()
            return node
        
    def expr(self):
        node = self.term()
        
        while self.currentToken.type in [PLUS, MINUS]:
            token = self.currentToken
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:  
                self.eat(MINUS)

            node = BinOp(node, token, self.term())

        return node 
    
    def term(self):
        node = self.factor()

        while self.currentToken.type in [MUL, DIV, INTDIV]:
            token = self.currentToken
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == INTDIV:
                self.eat(INTDIV)

            node = BinOp(node, token, self.factor())
  
        return node
    
    def parse(self):
        node = self.program()
        if self.currentToken.type != EOF:
            self.error()
            
        return node 
        