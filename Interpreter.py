from Token import *
from Constants import *
from collections import deque

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.currentToken = None
    
    def error(self):
        raise Exception("Error parsing input")

    #for calculating numerical operations    
    def operatorPrecedence(self, op) -> int:
        if op == '^':
            return 3
        elif op == '*' or op == '/':
            return 2
        elif op == '+' or op == '-':
            return 1
        
        return -1

    def infixToPostfix(self, tokens: list[Token]) -> list[Token]:
        operators = deque()
        postfix = []

        for token in tokens:
            if token.type == INTEGER:
                postfix.append(token)
            elif token.value == '(':
                operators.append(token)
            elif token.value == ')':
                while len(operators) != 0 and operators[-1].value != '(':
                    top = operators.pop()
                    postfix.append(top)
                if len(operators) != 0:
                    operators.pop()
            else:
                print(self.operatorPrecedence(token.value))
                while (len(operators) != 0 and self.operatorPrecedence(token.value) <= self.operatorPrecedence(operators[-1].value)):
                    top = operators.pop()
                    postfix.append(top)
                operators.append(token)

        while len(operators) != 0:
            top = operators.pop()
            postfix.append(top)

        return postfix

    def getNextToken(self):
        if self.pos > len(self.text) - 1:
            self.pos += 1
            return Token(EOF, None)

        c = self.text[self.pos]
        self.pos += 1
        if c == " " or c == "\t":
            return self.getNextToken()

        if c.isdigit():
            num = "" 
            while c.isdigit(): 
                num += c
                if self.pos < len(self.text):
                    if self.text[self.pos].isdigit():
                        c = self.text[self.pos]
                        self.pos += 1
                    else:
                        break
                else:
                    break
                
            return Token(INTEGER, int(num))

        elif c == '+':
            return Token(PLUS, c)

        elif c == '-':
            return Token(MINUS, c)
        
        elif c == '*':
            return Token(TIMES, c)
        
        elif c == '/':
            return Token(DIVIDE, c)

        self.error()

    def eat(self, tokenType):
        if self.currentToken.type == tokenType:
            self.currentToken = self.getNextToken()
        else:
            self.error()

    def expr(self):
        #TODO: add subtraction
        self.currentToken = self.getNextToken()
        left = self.currentToken
        self.eat(INTEGER)
        operator = self.currentToken
        if operator.type == PLUS:
            self.eat(PLUS)
            right = self.currentToken
            self.eat(INTEGER)

            return left.value + right.value

        elif operator.type == MINUS:
            self.eat(MINUS)
            right = self.currentToken
            self.eat(INTEGER)

            return left.value - right.value 
        
        elif operator.type == TIMES:
            self.eat(TIMES)
            right = self.currentToken
            self.eat(INTEGER)

            return left.value * right.value
        
        elif operator.type == DIVIDE:
            self.eat(DIVIDE)
            right = self.currentToken
            self.eat(INTEGER)

            return left.value / right.value


if __name__ == "__main__":
    interpreter = Interpreter("20 + 20 - 8 * 9")
    token = Token(None, None)
    tokens = []
    
    while token.type != EOF:
        token = interpreter.getNextToken()
        if token.type == EOF:
            break
        tokens.append(token)
    print(tokens)
    postfix = interpreter.infixToPostfix(tokens)
    prefix = postfix[::-1]

    for i in prefix:
        print(i.value, end=" ")