# SISTEMA DE TIPOS Y OBJETOS DEL INTERPRETE

class ObjType:
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    NULL = "NULL"
    RETURN_VALUE = "RETURN_VALUE"
    ERROR = "ERROR"
    FUNCTION = "FUNCTION"
    ARRAY = "ARRAY"
    BUILTIN = "BUILTIN"
    BREAK_VALUE = "BREAK_VALUE"

class Obj:
    def type(self): pass
    def inspect(self): pass

class Integer(Obj):
    def __init__(self, value):
        self.value = value
    def type(self): return ObjType.INTEGER
    def inspect(self): return str(self.value)

class StringObj(Obj):
    def __init__(self, value):
        self.value = value
    def type(self): return ObjType.STRING
    def inspect(self): return self.value

class BooleanVal(Obj):
    def __init__(self, value):
        self.value = value
    def type(self): return ObjType.BOOLEAN
    def inspect(self): return "true" if self.value else "false"

class Null(Obj):
    def type(self): return ObjType.NULL
    def inspect(self): return "null"

class ReturnValue(Obj):
    def __init__(self, value):
        self.value = value
    def type(self): return ObjType.RETURN_VALUE
    def inspect(self): return self.value.inspect()

class BreakValue(Obj):
    def type(self): return ObjType.BREAK_VALUE
    def inspect(self): return "break"

class Error(Obj):
    def __init__(self, message):
        self.message = message
    def type(self): return ObjType.ERROR
    def inspect(self): return f"ERROR: {self.message}"

class FunctionObj(Obj):
    def __init__(self, parameters, body, env):
        self.parameters = parameters
        self.body = body
        self.env = env
    def type(self): return ObjType.FUNCTION
    def inspect(self):
        params = ", ".join([p.value for p in self.parameters])
        return f"fn({params}) {{ ... }}"

class ArrayObj(Obj):
    def __init__(self, elements):
        self.elements = elements
    def type(self): return ObjType.ARRAY
    def inspect(self):
        return "[" + ", ".join([e.inspect() for e in self.elements]) + "]"

class Builtin(Obj):
    def __init__(self, fn):
        self.fn = fn
    def type(self): return ObjType.BUILTIN
    def inspect(self): return "builtin function"
