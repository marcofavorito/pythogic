from abc import ABC, abstractmethod

from pythogic.misc.Symbol import PredicateSymbol
from pythogic.fol.syntax.Term import Term, Variable


class FOLFormula(ABC):
    def evaluate(self):
        raise NotImplementedError

    def __invert__(self):
        return Not(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __rshift__(self, other):
        return Implies(self, other)

    def containsVariable(self, v:Variable):
        return NotImplementedError

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




class PredicateFOLFormula(FOLFormula):
    def __init__(self, predicate_symbol: PredicateSymbol, *args: Term):
        assert len(args) == predicate_symbol.arity
        self.predicate_symbol = predicate_symbol
        self.args = args

    def __str__(self):
        return str(self.predicate_symbol) + "(" + ", ".join([t.__str__() for t in self.args]) + ")"


    def _members(self):
        return (self.predicate_symbol, *self.args)

    @classmethod
    def fromString(cls, name: str, *args: Term):
        return PredicateFOLFormula(PredicateSymbol(name, len(args)), *args)

    def containsVariable(self, v:Variable):
        return v in self.args


class Operator(FOLFormula):
    @property
    def operator_symbol(self):
        raise NotImplementedError

class UnaryOperator(Operator):
    def __init__(self, f: FOLFormula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + "(" + str(self.f) + ")"

    def _members(self):
        return (self.operator_symbol, self.f)

class BinaryOperator(Operator):
    """A generic binary formula"""

    def __init__(self, f1:FOLFormula, f2:FOLFormula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

    def containsVariable(self, v:Variable):
        return self.f1.containsVariable(v) or self.f2.containsVariable(v)

    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)


class QuantifiedFormula(Operator):
    def __init__(self, v: Variable, f: FOLFormula):
        self.v = v
        self.f = f

    def containsVariable(self, v: Variable):
        return self.f.containsVariable(v)

    def _members(self):
        return (self.operator_symbol, self.v, self.f)

    def __str__(self):
        return self.operator_symbol + str(self.v) + "." + str(self.f)


class Equal(Operator):
    """Equality operator: term_1 = term_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Equal(a, b)
        >>> str(e)
        'a = b'
    """
    operator_symbol = "="
    def __init__(self, t1: Term, t2: Term):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return str(self.t1) + " = " + str(self.t2)

    def containsVariable(self, v:Variable):
        return self.t1 == v or self.t2 == v

    def _members(self):
        return (self.t1, self.operator_symbol, self.t2)


class Not(UnaryOperator):
    """Negation operator: ~formula

    >>> a=Variable.fromString("a")
    >>> A=PredicateFOLFormula.fromString("A", a)
    >>> e = Not(A)
    >>> str(e)
    '~(A^1(a))'

    """
    operator_symbol = "~"



class And(BinaryOperator):
    """And operator: formula_1 & formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> A=PredicateFOLFormula.fromString("A", a); B=PredicateFOLFormula.fromString("B", b)
        >>> e = And(a, b)
        >>> str(e)
        'a & b'
    """
    operator_symbol = "&"
    def __init__(self, f1: FOLFormula, f2: FOLFormula):
        super().__init__(f1, f2)

    def __str__(self):
        return super().__str__()


class Or(BinaryOperator):
    """Or operator: formula_1 | formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Or(a, b)
        >>> str(e)
        'a | b'
    """
    operator_symbol = "|"
    def __init__(self, f1: FOLFormula, f2: FOLFormula):
        super().__init__(f1, f2)


    def __str__(self):
        return super().__str__()


class Implies(BinaryOperator):
    """Logical implication: formula_1 >> formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Implies(a, b)
        >>> str(e)
        'a >> b'
    """

    operator_symbol = ">>"
    def __init__(self, f1: FOLFormula, f2: FOLFormula):
        super().__init__(f1, f2)

    def __str__(self):
        return super().__str__()


class Exists(QuantifiedFormula):

    operator_symbol = "∃"
    def __init__(self, v: Variable, f: FOLFormula):
        super().__init__(v, f)


class ForAll(QuantifiedFormula):

    operator_symbol = "Ɐ"
    def __init__(self, v: Variable, f: FOLFormula):
        super().__init__(v, f)
