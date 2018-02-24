# -*- coding: utf-8 -*-

"""Module for First-Order logic
For the theory please see: http://mathworld.wolfram.com/First-OrderLogic.html
"""


from typing import Set

from pythogic.fol.syntax.FOLFormula import FOLFormula, PredicateFOLFormula, Equal, Not, And, Or, Implies, Exists, \
    ForAll, UnaryOperator, BinaryOperator, QuantifiedFormula
from pythogic.misc.Symbol import FunctionSymbol, PredicateSymbol
from pythogic.fol.syntax.Term import Term, Variable, FunctionTerm


class FOL(object):
    """Class to represent a FOL formal system"""

    def __init__(self, functions: Set[FunctionSymbol], predicates: Set[PredicateSymbol]):
        self.functions = functions
        self.predicates = predicates


    def _is_term(self, t: Term):
        """Check if a term is legal in the current formal system"""
        if isinstance(t, Variable):
            return True
        elif isinstance(t, FunctionTerm):
            return isinstance(t.symbol, FunctionSymbol) \
                   and t.symbol in self.functions \
                   and all(self._is_term(arg) for arg in t.args)
        else:
            raise ValueError("Argument neither a Variable nor a FunctionTerm")

    def _is_formula(self, f: FOLFormula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, PredicateFOLFormula):
            return f.predicate_symbol in self.predicates and all(self._is_term(t) for t in f.args)
        elif isinstance(f, Equal):
            return self._is_term(f.t1) and self._is_term(f.t2)
        elif isinstance(f, UnaryOperator):
            return self._is_formula(f.f)
        elif isinstance(f, BinaryOperator):
            return self._is_formula(f.f1) and self._is_formula(f.f2)
        elif isinstance(f, QuantifiedFormula):
            return isinstance(f.v, Variable) and self._is_formula(f.f)
        else:
            raise ValueError("Argument not a valid Formula")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
