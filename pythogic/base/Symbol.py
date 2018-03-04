# -*- coding: utf-8 -*-

class Symbol(object):
    """A class to represent a symbol (actually, a wrap for a string)"""
    def __init__(self, name: str):
        self.name = str(name)

    def __str__(self):
        return self.name

    def _members(self):
        return (self.name)

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())

    def __repr__(self):
        return ", ".join(map(str,self._members()))

    def __lt__(self, other):
        return self.name.__lt__(other.name)



class FunctionSymbol(Symbol):
    """A class to represent a function symbol ("""
    def __init__(self, name: str, arity: int):
        super().__init__(name)
        self.arity = arity

    def __str__(self):
        return self.name + "^" + str(self.arity)

    def _members(self):
        return (self.name, self.arity)


class ConstantSymbol(FunctionSymbol):
    def __init__(self, name:str):
        super().__init__(name, 0)


class PredicateSymbol(Symbol):
    def __init__(self, name: str, arity):
        super().__init__(name)
        self.arity = arity

    def __str__(self):
        return self.name + "^" + str(self.arity)

    def __repr__(self):
        return self.name + "^" + str(self.arity)

    def _members(self):
        return (self.name, self.arity)


class TrueSymbol(Symbol):
    def __init__(self):
        super().__init__("⊤")

class FalseSymbol(Symbol):
    def __init__(self):
        super().__init__("⊥")

class LastSymbol(Symbol):
    def __init__(self):
        super().__init__("Last")


DUMMY_SYMBOL = Symbol("dummy_proposition")