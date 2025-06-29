from Parser import *
from Interpreter import *

num = 0

if num == 1:
    text = input(">> ")
    while text != "quit":
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser) 
        result = interpreter.interpret()
            
        print(interpreter.GLOBAL_SCOPE) 
        text = input(">> ") 
    
else:
    text = """\
     PROGRAM Part10;
VAR
   number     : INTEGER;
   a, b, c, x : INTEGER;
   y          : REAL;

BEGIN {Part10}
   BEGIN
      number := 2;
      a := number;
      b := 10 * a + 10 * number DIV 4;
      c := a - - b
   END;
   x := 11;
   y := 20 / 7 + 3.14;
   { writeln('a = ', a); }
   { writeln('b = ', b); }
   { writeln('c = ', c); }
   { writeln('number = ', number); }
   { writeln('x = ', x); }
   { writeln('y = ', y); }
END.  {Part10}
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)
