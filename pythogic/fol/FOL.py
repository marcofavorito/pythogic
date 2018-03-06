# -*- coding: utf-8 -*-

"""Module for First-Order logic
For the theory please see: http://mathworld.wolfram.com/First-OrderLogic.html
"""


from pythogic.base.FormalSystem import FormalSystem
from pythogic.fol.semantics.Assignment import Assignment
from pythogic.fol.syntax.FOLAlphabet import FOLAlphabet
from pythogic.base.Formula import PredicateFormula, Equal, Not, \
    And, Or, Implies, Exists, ForAll, Formula, Equivalence, FalseFormula, TrueFormula, DUMMY_TERM
from pythogic.base.Symbol import FunctionSymbol
from pythogic.fol.syntax.Term import Term, Variable, FunctionTerm


class FOL(FormalSystem):
    """Class to represent a FOL formal system"""

    def __init__(self, alphabet: FOLAlphabet):
        super().__init__(alphabet)

    allowed_formulas = {PredicateFormula, Equal, Not, And, Exists}
    derived_formulas = {Or, Implies, Equivalence, ForAll, TrueFormula, FalseFormula}

    def _is_term(self, t: Term):
        """Check if a term is legal in the current FOL formal system"""
        if t==DUMMY_TERM:
            return True
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
        elif isinstance(f, Not):
            return self.is_formula(f.f)
        elif isinstance(f, And):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, Exists):
            return isinstance(f.v, Variable) and self.is_formula(f.f)
        else:
            return False

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

    def to_equivalent_formula(self, derived_formula:Formula):
        if isinstance(derived_formula, Or):
            return Not(And(Not(derived_formula.f1), Not(derived_formula.f2)))
        elif isinstance(derived_formula, Implies):
            return Not(And(derived_formula.f1, Not(derived_formula.f2)))
        elif isinstance(derived_formula, Equivalence):
            positive_equivalence = And(derived_formula.f1, derived_formula.f2)
            negative_equivalence = And(Not(derived_formula.f1), Not(derived_formula.f2))
            return Not(And(Not(positive_equivalence), Not(negative_equivalence)))
        elif isinstance(derived_formula, FalseFormula):
            return Not(Equal(DUMMY_TERM, DUMMY_TERM))
        elif isinstance(derived_formula, TrueFormula):
            return Equal(DUMMY_TERM, DUMMY_TERM)
        elif isinstance(derived_formula, ForAll):
            return Not(Exists(derived_formula.v, Not(derived_formula.f)))
        elif derived_formula in self.allowed_formulas:
            return derived_formula
        else:
            raise ValueError("Derived formula not recognized")

    def _expand_formula(self, f:Formula):
        if isinstance(f, PredicateFormula) or isinstance(f, Equal):
            return f
        elif isinstance(f, And):
            return And(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Not):
            return Not(self.expand_formula(f.f))
        elif isinstance(f, Exists):
            return Exists(f.v, self.expand_formula(f.f))
        else:
            raise ValueError("Not valid Formula to expand.")

    # def contains_variable(self, f:Formula, v:Variable):
    #     formula = f
    #     if isinstance(formula, PredicateFormula):
    #         return v in formula.args
    #     elif isinstance(formula, Equal):
    #         return v == formula.t1 or v == formula.t2
    #     elif isinstance(formula, Not):
    #         return self.contains_variable(formula.f, v)
    #     elif isinstance(formula, And):
    #         return self.contains_variable(formula.f1, v) or self.contains_variable(formula.f2, v)
    #     elif isinstance(formula, Exists):
    #         return self.contains_variable(formula.f, v)
    #     else:
    #         raise ValueError("Not valid formula to check.")

    def to_nnf(self, f:Formula):
        assert self.is_formula(f)
        formula = self.expand_formula(f)

        if isinstance(formula, PredicateFormula) or isinstance(formula, Equal):
            return formula
        elif isinstance(formula, And):
            return And(self.to_nnf(formula.f1), self.to_nnf(formula.f2))
        if isinstance(formula, Exists):
            return Exists(formula.v, self.to_nnf(formula.f))
        if isinstance(formula, Not):
            subformula = formula.f
            if isinstance(subformula, Not):
                return self.to_nnf(subformula.f)
            elif isinstance(subformula, And):
                return Or(self.to_nnf(Not(subformula.f1)), self.to_nnf((Not(subformula.f2))))
            elif isinstance(subformula, Exists):
                return ForAll(subformula.v, self.to_nnf(Not(subformula.f)))
            elif isinstance(subformula, PredicateFormula) or isinstance(subformula, Equal):
                return formula
            else:
                raise ValueError
        else:
            raise ValueError

if __name__ == '__main__':
    import doctest

    doctest.testmod()
