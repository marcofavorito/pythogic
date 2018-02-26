"""Propositional Logic"""

from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.base.Symbol import DUMMY_SYMBOL
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.base.Formula import AtomicFormula, TrueFormula, FalseFormula, Formula, Not, Or, And, Implies


class PL(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {AtomicFormula, Not, And}
    derived_formulas = {Or, Implies, TrueFormula, FalseFormula}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, AtomicFormula):
            return f.symbol in self.alphabet.symbols or f.symbol == DUMMY_SYMBOL
        elif isinstance(f, Not):
            return self.is_formula(f.f)
        elif isinstance(f, And):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        else:
            raise ValueError("Argument not a valid Formula")

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


    @staticmethod
    def _from_finite_trace(trace:FiniteTrace, position:int):
        symbol2truth = {e: True if AtomicFormula(e) in trace.get(position) else False for e in trace.alphabet.symbols}
        I = PLInterpretation(trace.alphabet, symbol2truth)
        pl = PL(trace.alphabet)
        return pl, I

