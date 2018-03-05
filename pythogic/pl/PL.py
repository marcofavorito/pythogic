"""Propositional Logic"""
from typing import Set

from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.base.Symbol import DUMMY_SYMBOL, Symbol
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.base.Formula import AtomicFormula, TrueFormula, FalseFormula, Formula, Not, Or, And, Implies, \
    DUMMY_ATOMIC, Equivalence


class PL(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {AtomicFormula, Not, And}
    derived_formulas = {Or, Implies, Equivalence, TrueFormula, FalseFormula}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, AtomicFormula):
            return f.symbol in self.alphabet.symbols or f.symbol == DUMMY_SYMBOL
        elif isinstance(f, Not):
            return self.is_formula(f.f)
        elif isinstance(f, And):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        else:
            return False

    def _truth(self, formula: Formula, interpretation: PLInterpretation):
        assert self._is_formula(formula)
        truth = self.truth
        if isinstance(formula, AtomicFormula):
            try:
                return interpretation.symbol2truth[formula.symbol]
            except:
                return False
        elif isinstance(formula, Not):
            return not truth(formula.f, interpretation)
        elif isinstance(formula, And):
            return truth(formula.f1, interpretation) and truth(formula.f2, interpretation)
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
            return And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        elif isinstance(derived_formula, TrueFormula):
            return Not(And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC))
        elif derived_formula in self.allowed_formulas:
            return derived_formula
        else:
            raise ValueError("Derived formula not recognized")

    def _expand_formula(self, f:Formula):
        if isinstance(f, AtomicFormula):
            return f
        elif isinstance(f, And):
            return And(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Not):
            return Not(self.expand_formula(f.f))
        elif type(f) in self.derived_formulas:
            return self.expand_formula(self.to_equivalent_formula(f))
        else:
            raise ValueError("Formula to expand not recognized")

    @staticmethod
    def _from_set_of_propositionals(props:Set[AtomicFormula], alphabet:Alphabet):
        symbol2truth = {e: True if AtomicFormula(e) in props else False for e in alphabet.symbols}
        I = PLInterpretation(alphabet, symbol2truth)
        pl = PL(alphabet)
        return pl, I


    def to_nnf(self, f:Formula):
        assert self.is_formula(f)
        formula = self.expand_formula(f)
        # formula = self.expand_formula(f)
        if isinstance(formula, AtomicFormula):
            return formula
        elif isinstance(formula, And):
            return And(self.to_nnf(formula.f1), self.to_nnf(formula.f2))
        elif isinstance(formula, Not):
            subformula = formula.f
            if isinstance(subformula, Not):
                return self.to_nnf(subformula.f)
            elif isinstance(subformula, And):
                return Or(self.to_nnf(Not(subformula.f1)), self.to_nnf((Not(subformula.f2))))
            elif isinstance(subformula, AtomicFormula):
                return formula
            else:
                raise ValueError
        else:
            raise ValueError

