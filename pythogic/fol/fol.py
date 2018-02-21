# -*- coding: utf-8 -*-

"""Module for First-Order logic
For the theory please see: http://mathworld.wolfram.com/First-OrderLogic.html
"""


from typing import Set
from abc import ABC

from pythogic.fol.Symbol import Symbol, FunctionSymbol, ConstantSymbol, PredicateSymbol

class Term(object):
    def __init__(self, symbol: Symbol):
        self.symbol = symbol

    def __str__(self):
        return str(self.symbol)

    def __eq__(self, other):
        return Equal(self, other)

    def __hash__(self):
        return self.symbol.__hash__()


class Variable(Term):
    def __init__(self, symbol: Symbol):
        super().__init__(symbol)


    @classmethod
    def fromString(cls, name:str):
        return Variable(Symbol(name))




class FunctionTerm(Term):
    def __init__(self, function_symbol: FunctionSymbol, *args:Term):
        assert len(args) == function_symbol.arity
        super().__init__(function_symbol)
        self.args = args

    def __str__(self):
        return super().__str__() + "(" + ", ".join([t.__str__() for t in self.args]) + ")"



class ConstantTerm(FunctionTerm):
    def __init__(self, constant_symbol: ConstantSymbol):
        super().__init__(constant_symbol)



class Formula(ABC):
    def evaluate(self):
        raise NotImplementedError

    def __invert__(self):
        return Negate(self)

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __rshift__(self, other):
        return Implies(self, other)


class PredicateFormula(Formula):
    def __init__(self, predicate_symbol: PredicateSymbol, *args:Term):
        assert len(args) == predicate_symbol.arity
        self.predicate_symbol = predicate_symbol
        self.args = args

    def __str__(self):
        return str(self.predicate_symbol) + "(" + ", ".join([t.__str__() for t in self.args]) + ")"

    @classmethod
    def fromString(cls, name: str, *args:Term):
        return PredicateFormula(PredicateSymbol(name, len(args)), *args)

class Operator(Formula):
    @property
    def operator_symbol(self):
        raise NotImplementedError




class BinaryOperator(Operator):
    """A generic binary formula"""

    def __init__(self, f1:Formula, f2:Formula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

class Equal(Operator):
    """Equality operator: term_1 = term_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Equal(a, b)
        >>> str(e)
        'a = b'
    """
    operator_symbol = "="
    def __init__(self, t1:Term, t2:Term):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return str(self.t1) + " = " + str(self.t2)


class Negate(Formula):
    """Negation operator: ~formula

    >>> a=Variable.fromString("a")
    >>> A=PredicateFormula.fromString("A", a)
    >>> e = Negate(A)
    >>> str(e)
    '~(A^1(a))'

    """
    operator_symbol = "~"
    def __init__(self, f:Formula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + "(" + str(self.f) + ")"


class And(BinaryOperator):
    """And operator: formula_1 & formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> A=PredicateFormula.fromString("A", a); B=PredicateFormula.fromString("B", b)
        >>> e = And(a, b)
        >>> str(e)
        'a & b'
    """
    operator_symbol = "&"
    def __init__(self, f1: Formula, f2: Formula):
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
    def __init__(self, f1: Formula, f2: Formula):
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
    def __init__(self, f1: Formula, f2: Formula):
        super().__init__(f1, f2)

    def __str__(self):
        return super().__str__()

class Exists(Formula):
    def __init__(self, v: Variable, t: Term):
        self.v = v
        self.t = t

class ForAll(Formula):
    def __init__(self, v: Variable, t: Term):
        self.v = v
        self.t = t


class FOL(object):
    """Class to represent a FOL formal system"""

    def __init__(self, vars: Set[Variable], functions: Set[FunctionSymbol], predicates: Set[PredicateSymbol]):
        self.vars = vars
        self.functions = functions
        self.predicates = predicates


    def _is_term(self, t:Term):
        """Check if a term is legal in the current formal system"""
        if isinstance(t, Variable):
            return t in self.vars
        if isinstance(t, FunctionTerm):
            return isinstance(t.symbol, FunctionSymbol) \
                   and t.symbol in self.functions \
                   and all(self._is_term(arg) for arg in t.args)
        else:
            raise ValueError("Argument neither a Variable nor a FunctionTerm")

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, PredicateFormula):
            return f.predicate_symbol in self.predicates and all(self._is_term(t) for t in f.args)
        elif isinstance(f, Equal):
            return self._is_term(f.t1) and self._is_term(f.t2)
        elif isinstance(f, Negate):
            return self._is_formula(f.f)
        elif any(isinstance(f, op) for op in [And, Or, Implies]):
            return self._is_formula(f.f1) and self._is_formula(f.f2)
        elif any(isinstance(f, quantification) for quantification in [Exists, ForAll]):
            return f.v in self.vars and self._is_formula(f.f)
        else:
            return False








if __name__ == '__main__':
    import doctest
    doctest.testmod()
