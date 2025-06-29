from Token import *
from Constants import *
from Lexer import *
from AST import *
from collections import deque

class Parser(object):
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer 
        self.currentToken = self.lexer.getNextToken() 
    
    def error(self) -> None:
        raise Exception("Error parsing input")

    def eat(self, tokenType: str) -> None:
        if self.currentToken.type == tokenType:
            self.currentToken = self.lexer.getNextToken()
        else:
            self.error()

    def program(self) -> Program:
        self.eat(PROGRAM)
        varNode = self.variable()
        programName = varNode.value
        self.eat(SEMI)
        blockNode = self.block()
        self.eat(DOT)
        programNode = Program(programName, blockNode)
        
        return programNode  

    def block(self) -> Block:
        declarationNodes = self.declarations()
        compoundStatementNodes = self.compoundStatement() 
        node = Block(declarationNodes, compoundStatementNodes)

        return node

    def declarations(self):
        declarations = []
        if self.currentToken.type == VAR:
            self.eat(VAR)
            while self.currentToken.type == ID:
                varDecl = self.variableDeclaration()
                declarations.extend(varDecl)
                self.eat(SEMI)

        while self.currentToken.type == PROCEDURE:
            self.eat(PROCEDURE)
            procName = self.currentToken.value
            self.eat(ID)
            self.eat(SEMI)
            blockNode = self.block()
            procDecl = ProcedureDecl(procName, blockNode)
            declarations.append(procDecl)
            self.eat(SEMI)
        
        return declarations 

    def variableDeclaration(self) -> list[VarDecl]:
        varNodes = [Var(self.currentToken)]
        self.eat(ID)

        while self.currentToken.type == COMMA:
            self.eat(COMMA)
            varNodes.append(Var(self.currentToken))
            self.eat(ID)

        self.eat(COLON)

        typeNode = self.typeSpec()
        varDeclarations = [VarDecl(varNode, typeNode) for varNode in varNodes]

        return varDeclarations 

    def typeSpec(self) -> Type:
        token = self.currentToken 
        if self.currentToken.type == INTEGER:
            self.eat(INTEGER)
        elif self.currentToken.type == REAL:
            self.eat(REAL)
        node = Type(token)
        
        return node

    def compoundStatement(self) -> Compound:
        self.eat(BEGIN)
        nodes = self.statementList()
        self.eat(END) 

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root 

    def statementList(self) -> list:
        node = self.statement()
        results = [node]

        while self.currentToken.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        
        if self.currentToken.type == ID:
            self.error()
        
        return results

    def statement(self) -> Union[Compound, Assign, NoOp]:
        if self.currentToken.type == BEGIN:
            return self.compoundStatement() 
        elif self.currentToken.type == ID:
            return self.assignmentStatement()
        else:
            node = self.empty()

        return node

    def assignmentStatement(self) -> Assign:
        left = self.variable()
        token = self.currentToken
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)

        return node

    def variable(self) -> Var:
        node = Var(self.currentToken)
        self.eat(ID)

        return node 

    def empty(self) -> NoOp:
        return NoOp()

    def factor(self) -> Union[Num, UnaryOp, BinOp, Var]:
        token = self.currentToken

        if token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
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
        
    def expr(self) -> Union[Num, UnaryOp, BinOp, Var]:
        node = self.term()
        
        while self.currentToken.type in [PLUS, MINUS]:
            token = self.currentToken
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:  
                self.eat(MINUS)

            node = BinOp(node, token, self.term())

        return node 
    
    def term(self) -> Union[Num, UnaryOp, BinOp, Var]:
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
    
    def parse(self) -> Program:
        node = self.program()
        if self.currentToken.type != EOF:
            self.error()
            
        return node 
        