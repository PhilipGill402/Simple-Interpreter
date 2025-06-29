from Parser import *
from Interpreter import *

with open("text.txt") as f:
    text = f.read()

lexer = Lexer(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
interpreter.interpret()
print(interpreter.GLOBAL_SCOPE)
