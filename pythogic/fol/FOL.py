# -*- coding: utf-8 -*-

"""Module for First-Order logic
For the theory please see: http://mathworld.wolfram.com/First-OrderLogic.html
"""


from typing import Set

from pythogic.fol.semantics.Assignment import Assignment
from pythogic.fol.syntax.FOLAlphabet import FOLAlphabet
from pythogic.fol.syntax.FOLFormula import FOLFormula, PredicateFOLFormula, Equal, Not, And, Or, Implies, Exists, \
    ForAll, UnaryOperator, BinaryOperator, QuantifiedFormula
from pythogic.misc.Symbol import FunctionSymbol, PredicateSymbol
from pythogic.fol.syntax.Term import Term, Variable, FunctionTerm


class FOL(object):
    """Class to represent a FOL formal system"""

    def __init__(self, alphabet:FOLAlphabet):
        self.alphabet = alphabet


    def _is_term(self, t: Term):
        """Check if a term is legal in the current formal system"""
        if isinstance(t, Variable):
            return True
        elif isinstance(t, FunctionTerm):
            return isinstance(t.symbol, FunctionSymbol) \
                   and t.symbol in self.alphabet.functions \
                   and all(self._is_term(arg) for arg in t.args)
        else:
            raise ValueError("Argument neither a Variable nor a FunctionTerm")

    def _is_formula(self, f: FOLFormula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, PredicateFOLFormula):
            return f.predicate_symbol in self.alphabet.predicates and all(self._is_term(t) for t in f.args)
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

    def truth(self, assignment: Assignment, formula: FOLFormula):
        assert self._is_formula(formula)
        truth = self.truth
        if isinstance(formula, Equal):
            return assignment(formula.t1) == assignment(formula.t2)
        elif isinstance(formula, PredicateFOLFormula):
            return tuple(assignment(t) for t in formula.args) in assignment.interpretation.getRelation(
                formula.predicate_symbol).tuples
        elif isinstance(formula, Not):
            return not truth(assignment, formula.f)
        elif isinstance(formula, And):
            return truth(assignment, formula.f1) and truth(assignment, formula.f2)
        elif isinstance(formula, Or):
            return truth(assignment, formula.f1) or truth(assignment, formula.f2)
        elif isinstance(formula, Implies):
            return not truth(assignment, formula.f1) or truth(assignment, formula.f2)
        elif isinstance(formula, Exists):
            # assert formula.v not in assignment.variable2object
            res = False
            for el in assignment.interpretation.domain:
                new_mapping = assignment.variable2object.copy()
                new_mapping[formula.v] = el
                res = res or truth(Assignment(new_mapping, assignment.interpretation), formula.f)
                if res: break
            return res
        elif isinstance(formula, ForAll):
            # assert formula.v not in assignment.variable2object
            res = True
            for el in assignment.interpretation.domain:
                new_mapping = assignment.variable2object.copy()
                new_mapping[formula.v] = el
                res = res and truth(Assignment(new_mapping, assignment.interpretation), formula.f)
                if not res: break
            return res
        else:
            raise ValueError("Formula not recognized")

if __name__ == '__main__':
    import doctest
    doctest.testmod()
