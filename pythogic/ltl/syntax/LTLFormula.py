from abc import ABC, abstractmethod

from pythogic.misc.Symbol import Symbol, TrueSymbol, FalseSymbol


class LTLFormula(ABC):

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


class LTLAtomicProposition(LTLFormula):

    def __init__(self, symbol:Symbol):
        self.symbol = symbol

    def _members(self):
        return (self.symbol)

    def __str__(self):
        return str(self.symbol)


class LTLTrue(LTLAtomicProposition):
    def __init__(self):
        super().__init__(TrueSymbol())


class LTLFalse(LTLAtomicProposition):
    def __init__(self):
        super().__init__(FalseSymbol())


class Operator(LTLFormula):
    @property
    def operator_symbol(self):
        raise NotImplementedError

class UnaryOperator(Operator):
    def __init__(self, f: LTLFormula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + "(" + str(self.f) + ")"

    def _members(self):
        return (self.operator_symbol, self.f)


class BinaryOperator(Operator):
    """A generic binary formula"""

    def __init__(self, f1:LTLFormula, f2:LTLFormula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)

class Not(Operator):
    """Negation operator: ~formula

    >>> a=LTLAtomicProposition(Symbol("a"))
    >>> e = Not(a)
    >>> str(e)
    '~(a)'

    """
    operator_symbol = "~"


#
class And(BinaryOperator):
    """And operator: formula_1 & formula_2

        >>> a=LTLAtomicProposition(Symbol("a")); b=LTLAtomicProposition(Symbol("b"))
        >>> e = And(a, b)
        >>> str(e)
        'a & b'
    """
    operator_symbol = "&"


class Or(BinaryOperator):
    """Or operator: formula_1 | formula_2

        >>> a=LTLAtomicProposition(Symbol("a")); b=LTLAtomicProposition(Symbol("b"))
        >>> e = Or(a, b)
        >>> str(e)
        'a | b'
    """
    operator_symbol = "|"

class Next(UnaryOperator):
    """Next operator: ○(formula_1) """
    operator_symbol = "○"

class Always(UnaryOperator):
    """Always operator: □(formula_1) """
    operator_symbol = "□"

class Eventually(UnaryOperator):
    """Eventually operator: ◇(formula_1) """
    operator_symbol = "◇"

class Until(BinaryOperator):
    """Until operator: U(formula_1) """
    operator_symbol = "U"

if __name__ == "__main__":

    import doctest
    doctest.testmod()
