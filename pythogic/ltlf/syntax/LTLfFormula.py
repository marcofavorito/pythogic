from abc import ABC, abstractmethod

from pythogic.misc.Symbol import Symbol, TrueSymbol, FalseSymbol, LastSymbol


class LTLfFormula(ABC):

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


class LTLfAtomicProposition(LTLfFormula):

    def __init__(self, symbol:Symbol):
        self.symbol = symbol

    def _members(self):
        return (self.symbol)

    def __str__(self):
        return str(self.symbol)


class Operator(LTLfFormula):
    @property
    def operator_symbol(self):
        raise NotImplementedError

class UnaryOperator(Operator):
    def __init__(self, f: LTLfFormula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + "(" + str(self.f) + ")"

    def _members(self):
        return (self.operator_symbol, self.f)


class BinaryOperator(Operator):
    """A generic binary formula"""

    def __init__(self, f1:LTLfFormula, f2:LTLfFormula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)

class Not(UnaryOperator):
    """Negation operator: ~formula

    >>> a=LTLfAtomicProposition(Symbol("a"))
    >>> e = Not(a)
    >>> str(e)
    '~(a)'

    """
    operator_symbol = "~"


#
class And(BinaryOperator):
    """And operator: formula_1 & formula_2

        >>> a=LTLfAtomicProposition(Symbol("a")); b=LTLfAtomicProposition(Symbol("b"))
        >>> e = And(a, b)
        >>> str(e)
        'a & b'
    """
    operator_symbol = "&"


class Next(UnaryOperator):
    """Next operator: ○(formula_1) """
    operator_symbol = "○"

class Until(BinaryOperator):
    """Until operator: U(formula_1) """
    operator_symbol = "U"


"""Derived operators"""
class DerivedLTLfFormula(LTLfFormula):
    def _equivalent_formula(self):
        raise NotImplementedError


class DerivedLTLfOperator(Operator):
    @property
    def operator_symbol(self):
        raise NotImplementedError


class DerivedLTLfBinaryOperator(Operator):
    """A generic binary formula"""

    def __init__(self, f1: LTLfFormula, f2: LTLfFormula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)


class DerivedLTLfUnaryOperator(Operator):
    def __init__(self, f: LTLfFormula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + "(" + str(self.f) + ")"

    def _members(self):
        return (self.operator_symbol, self.f)


class Or(DerivedLTLfBinaryOperator):
    """Or operator: formula_1 | formula_2

        >>> a=LTLfAtomicProposition(Symbol("a")); b=LTLfAtomicProposition(Symbol("b"))
        >>> e = Or(a, b)
        >>> str(e)
        'a | b'
    """
    operator_symbol = "|"
    def _equivalent_formula(self):
        return Not(And(Not(self.f1), Not(self.f2)))

class LTLfTrue(DerivedLTLfFormula):
    def _equivalent_formula(self):
        dummy_proposition = LTLfAtomicProposition(Symbol("dummy_proposition"))
        return Or(dummy_proposition, Not(dummy_proposition))

    def _members(self):
        return (TrueSymbol())

    def __str__(self):
        return str(TrueSymbol())



class LTLfFalse(DerivedLTLfFormula):
    def _equivalent_formula(self):
        dummy_proposition = LTLfAtomicProposition(Symbol("dummy_proposition"))
        return And(dummy_proposition, Not(dummy_proposition))

    def __str__(self):
        return str(FalseSymbol())

    def _members(self):
        return (FalseSymbol())

class LTLfLast(DerivedLTLfOperator):
    def __equivalent_formula(self):
        return Not(Next(LTLfTrue()))

    def _members(self):
        return (LastSymbol())

    def __str__(self):
        return str(LastSymbol())




class Eventually(DerivedLTLfUnaryOperator):
    """Eventually operator: ◇(formula_1) """
    operator_symbol = "◇"

    def _equivalent_formula(self):
        return Until(LTLfTrue(), self.f)


class Always(DerivedLTLfUnaryOperator):
    """Always operator: □(formula_1) """
    operator_symbol = "□"

    def _equivalent_formula(self):
        return Not(Eventually(Not(self.f)))






if __name__ == "__main__":
    import doctest
    doctest.testmod()
