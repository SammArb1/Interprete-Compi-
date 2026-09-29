# ENTORNO DE EJECUCION Y MEMORIA

class Environment:
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, name):
        obj = self.store.get(name)
        if obj is None and self.outer is not None:
            obj = self.outer.get(name)
        return obj

    def set(self, name, val):
        self.store[name] = val
        return val
        
    def assign(self, name, val):
        current = self
        while current is not None:
            if name in current.store:
                current.store[name] = val
                return val
            current = current.outer
        self.store[name] = val
        return val
