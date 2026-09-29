# EXPLICACIÓN DE CAMBIOS SUSTANCIALES
# ----------------------------------
# 1. Modificación de Arquitectura (Compilador -> Intérprete):
# Se reemplazó la fase de generación y emisión de código intermedio
# por un evaluador directo ("Tree-Walking Interpreter").
#
# 2. Entorno de Ejecución (Environment y Memoria):
# Se implementó la clase 'Environment', la cual usa diccionarios enlazados
# dinámicamente para manejar variables y permitir closures funcionales.
#
# 3. Flujo de Control Dinámico (Break, Return, Ciclos):
# Se modelaron estructuras devolviendo objetos 'ReturnValue' y 'BreakValue'
# para propagar saltos en la pila de evaluación de Python.
#
# 4. Modularización Organizada:
# El código fue separado en módulos (lexer, parser, ast_nodes, evaluator, etc.)

from repl import start_repl

if __name__ == "__main__":
    start_repl()
