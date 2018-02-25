# -*- coding: utf-8 -*-

"""Module for First-Order logic
For the theory please see: http://mathworld.wolfram.com/First-OrderLogic.html
"""


from pythogic.base.FormalSystem import FormalSystem
from pythogic.fol.semantics.Assignment import Assignment
from pythogic.fol.syntax.FOLAlphabet import FOLAlphabet
from pythogic.base.Formula import PredicateFormula, UnaryOperator, BinaryOperator, QuantifiedFormula, Equal, Not, \
    And, Or, Implies, Exists, ForAll, Formula
from pythogic.base.Symbol import FunctionSymbol
from pythogic.fol.syntax.Term import Term, Variable, FunctionTerm


class FOL(FormalSystem):
    """Class to represent a FOL formal system"""

    def __init__(self, alphabet: FOLAlphabet):
        super().__init__(alphabet)

    allowed_formulas = {PredicateFormula, Equal, Not, And, Exists}
    derived_formulas = {Or, Implies, ForAll}

    def _is_term(self, t: Term):
        """Check if a term is legal in the current FOL formal system"""
        if isinstance(t, Variable):
            return True
        elif isinstance(t, FunctionTerm):
            return isinstance(t.symbol, FunctionSymbol) \
                   and t.symbol in self.alphabet.functions \
                   and all(self._is_term(arg) for arg in t.args)
        else:
            raise ValueError("Argument neither a Variable nor a FunctionTerm")

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, PredicateFormula):
            return f.predicate_symbol in self.alphabet.predicates and all(self._is_term(t) for t in f.args)
        elif isinstance(f, Equal):
            return self._is_term(f.t1) and self._is_term(f.t2)
        elif isinstance(f, UnaryOperator):
            return self.is_formula(f.f)
        elif isinstance(f, BinaryOperator):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, QuantifiedFormula):
            return isinstance(f.v, Variable) and self.is_formula(f.f)
        else:
            raise ValueError("Argument not a valid Formula")

    def _truth(self, formula: Formula, assignment: Assignment):
        truth = self.truth
        if isinstance(formula, Equal):
            return assignment(formula.t1) == assignment(formula.t2)
        elif isinstance(formula, PredicateFormula):
            return tuple(assignment(t) for t in formula.args) in assignment.interpretation.getRelation(
                formula.predicate_symbol).tuples
        elif isinstance(formula, Not):
            return not truth(formula.f, assignment)
        elif isinstance(formula, And):
            return truth(formula.f1, assignment) and truth(formula.f2, assignment)
        elif isinstance(formula, Exists):
            # assert formula.v not in assignment.variable2object
            res = False
            for el in assignment.interpretation.domain:
                new_mapping = assignment.variable2object.copy()
                new_mapping[formula.v] = el
                res = res or truth(formula.f, Assignment(new_mapping, assignment.interpretation))
                if res: break
            return res
        else:
            raise ValueError("Formula not recognized")


if __name__ == '__main__':
    import doctest

    doctest.testmod()
