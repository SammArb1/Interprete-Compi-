# BUCLE INTERACTIVO

from lexer import Lexer
from parser import Parser
from environment import Environment
from evaluator import evaluate

def start_repl():
    env = Environment()
    print("--------------------------------------------")
    print("------ Bienvenido a la Patria Milagro ------")
    print("--------------------------------------------")
    print("Escribe código para evaluarlo al vuelo o 'exit' para salir.\n")
    while True:
        try:
            line = input(">> ")
            if line.strip() == "exit":
                break
            if line.strip() == "":
                continue
            lexer = Lexer(line)
            parser = Parser(lexer)
            program = parser.parse_program()
            
            if len(parser.errors) > 0:
                for msg in parser.errors:
                    print(f"ERROR SINTÁCTICO: {msg}")
                continue
                
            evaluated = evaluate(program, env)
            if evaluated is not None:
                print(evaluated.inspect())
                
        except EOFError:
            break
        except KeyboardInterrupt:
            break
