# -*- coding: utf-8 -*-

"""Module for First-Order logic
For the theory please see: http://mathworld.wolfram.com/First-OrderLogic.html
"""


from typing import Set

from pythogic.fol.syntax.Formula import Formula, PredicateFormula, Equal, Negate, And, Or, Implies, Exists, ForAll
from pythogic.fol.syntax.Symbol import FunctionSymbol, PredicateSymbol
from pythogic.fol.syntax.Term import Term, Variable, FunctionTerm


class FOL(object):
    """Class to represent a FOL formal system"""

    def __init__(self, vars: Set[Variable], functions: Set[FunctionSymbol], predicates: Set[PredicateSymbol]):
        self.vars = vars
        self.functions = functions
        self.predicates = predicates


    def _is_term(self, t: Term):
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
            raise ValueError("Argument not a valid Formula")








if __name__ == '__main__':
    import doctest
    doctest.testmod()
