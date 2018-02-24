from pythogic.misc.Formula import Formula
from pythogic.misc.Symbol import Symbol


class PLFormula(Formula):
    pass


class AtomicFormula(PLFormula):
    def __init__(self, symbol:Symbol):
        self.symbol = symbol

    def _members(self):
        return (self.symbol)

    def __str__(self):
        return str(self.symbol)

    def __lt__(self, other):
        return self.symbol.name.__lt__(other.symbol.name)

class Not(PLFormula):
    operator_symbol = "~"
    def __init__(self, f: PLFormula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + "(" + str(self.f) + ")"

    def _members(self):
        return (self.operator_symbol, self.f)


class And(PLFormula):

    operator_symbol = "&"
    def __init__(self, f1:PLFormula, f2:PLFormula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)


class Or(PLFormula):

    operator_symbol = "|"
    def __init__(self, f1:PLFormula, f2:PLFormula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)
