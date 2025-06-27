from Token import *
from Constants import *

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.c = self.text[self.pos] 
        self.RESERVED_KEYWORDS = {
                                    'begin': Token(BEGIN, 'begin'),
                                    'end': Token(END, 'end'),
                                    'div': Token(INTDIV, 'intdiv'),
                                    'program': Token(PROGRAM, 'program'),
                                    'var': Token(VAR, 'var'),
                                    'integer': Token(INTEGER, 'integer'),
                                    'real': Token(REAL, 'real')
                                }


    def _id(self):
        result = ''
        while self.c is not None and (self.c.isalnum() or self.c == '_'):
            result += self.c.lower()
            self.advance() 

        token = self.RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token 
    def error(self):
        raise Exception("Error parsing input")
    
    def peek(self):
        if self.pos+1 >= len(self.text):
            return None
        return self.text[self.pos+1]
    
    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.c = None 
        else:
            self.c = self.text[self.pos]

    
    def getNextToken(self):
        while self.c != None:
            #skips whitespace
            if self.c.isspace():
                self.advance()
                continue

            #skips comments
            if self.c == '{':
                while self.c != '}':
                    self.advance() 
                self.advance() 

            if self.c.isdigit():
                num = "" 
                while self.c.isdigit():
                    num += self.c
                    self.advance() 
                    
                return Token(INTEGER, int(num))

            elif self.c == '+':
                self.advance() 
                return Token(PLUS, self.c)

            elif self.c == '-':
                self.advance() 
                return Token(MINUS, self.c)
            
            elif self.c == '*':
                self.advance() 
                return Token(MUL, self.c)
            
            elif self.c == '/':
                self.advance() 
                return Token(DIV, self.c)
            
            elif self.c == '(':
                self.advance() 
                return Token(LPAREN, self.c)
            
            elif self.c == ')':
                self.advance() 
                return Token(RPAREN, self.c)
            
            elif self.c.isalpha() or self.c == '_':
                token = self._id()
                token.value = token.value.lower()

                return token 
            elif self.c == ':' and self.peek() == '=':
                self.advance()
                self.advance() 
                return Token(ASSIGN, ':=')
            
            elif self.c == ';':
                self.advance() 
                return Token(SEMI, ';')
            
            elif self.c == '.':
                self.advance() 
                return Token(DOT, '.')

        return Token(EOF, 'NONE')