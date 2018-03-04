from abc import abstractmethod, ABC

from pythogic.base.Symbol import Symbol, FunctionSymbol, ConstantSymbol


class Term(ABC):
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def __str__(self):
        return str(self.symbol)

    @abstractmethod
    def _members(self):
        return NotImplementedError

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())


class Variable(Term):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)

    def _members(self):
        return (self.symbol)

    @classmethod
    def fromString(cls, name:str):
        return Variable(Symbol(name))

    def __lt__(self, other):
        return self.symbol.__lt__(other.symbol)


class FunctionTerm(Term):
    def __init__(self, function_symbol: FunctionSymbol, *args:Term):
        assert len(args) == function_symbol.arity
        super().__init__(function_symbol)
        self.args = args

    def __str__(self):
        return super().__str__() + "(" + ", ".join([t.__str__() for t in self.args]) + ")"

    def _members(self):
        return (self.symbol, *self.args)


class ConstantTerm(FunctionTerm):
    def __init__(self, constant_symbol: ConstantSymbol):
        super().__init__(constant_symbol)

    @staticmethod
    def fromString(name:str):
        return ConstantTerm(ConstantSymbol(name))
