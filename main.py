import sys
import os

# Asegurar que el directorio de interprete_python esté en sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from lexer import Lexer
from parser import Parser
from environment import Environment
from evaluator import evaluate
from repl import start_repl
from objects import ObjType

def run_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: el archivo '{file_path}' no existe.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error al leer el archivo '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    lexer = Lexer(source_code)
    parser = Parser(lexer)
    program = parser.parse_program()

    if len(lexer.errors) > 0:
        print(f"Se encontraron {len(lexer.errors)} error(es) léxico(s):", file=sys.stderr)
        for err in lexer.errors:
            print(f"  {err}", file=sys.stderr)
        sys.exit(1)

    if len(parser.errors) > 0:
        print(f"Se encontraron {len(parser.errors)} error(es) sintáctico(s):", file=sys.stderr)
        for err in parser.errors:
            print(f"  {err}", file=sys.stderr)
        sys.exit(1)

    env = Environment()
    result = evaluate(program, env)

    if result is not None:
        if result.type() == ObjType.ERROR:
            print(result.inspect(), file=sys.stderr)
            sys.exit(1)
        if result.type() != ObjType.NULL:
            print(result.inspect())

    sys.exit(0)

def main():
    if len(sys.argv) == 1:
        start_repl()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print("Uso: python main.py [ruta_archivo]", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
