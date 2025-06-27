from Parser import *

num = 1

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
     BEGIN
        BEGIN
            number := 2;
            a := number;
            b := 10 * a + 10 * nUmber DIV 4;
            c := a - - b
        END;

        x := 11;
    END.
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)
