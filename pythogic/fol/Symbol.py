# -*- coding: utf-8 -*-

class Symbol(object):
    """A class to represent a symbol (actually, a wrap for a string)"""
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name



class FunctionSymbol(Symbol):
    """A class to represent a function symbol ("""
    def __init__(self, name: str, arity: int):
        super().__init__(name)
        self.arity = arity

    def __str__(self):
        return self.name + "^" + str(self.arity)



class ConstantSymbol(FunctionSymbol):
    def __init__(self, name:str):
        super().__init__(name, 0)


class PredicateSymbol(Symbol):
    def __init__(self, name: str, arity):
        super().__init__(name)
        self.arity = arity

    def __str__(self):
        return self.name + "^" + str(self.arity)
