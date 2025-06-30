from Parser import *
from Interpreter import *
from Symbol import *

with open("text.txt") as f:
    text = f.read()

lexer = Lexer(text)
parser = Parser(lexer)
tree = parser.parse()
symtabBuilder = SymbolTableBuilder()
try:
   symtabBuilder.visit(tree)
except Exception as e:
    print(e)

print(symtabBuilder.symtab)