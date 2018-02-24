"""Propositional Logic"""

from pythogic.misc.Alphabet import Alphabet
from pythogic.misc.FormalSystem import FormalSystem
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.pl.syntax.PLFormula import PLFormula, AtomicFormula, Not, Or, And


class PL(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    def _is_formula(self, f: PLFormula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, AtomicFormula):
            return f.symbol in self.alphabet.symbols
        elif isinstance(f, Not):
            return self._is_formula(f.f)
        elif isinstance(f, Or) or isinstance(f, And):
            return self._is_formula(f.f1) and self._is_formula(f.f2)
        else:
            raise ValueError("Argument not a valid Formula")

    def truth(self, interpretation: PLInterpretation, formula: PLFormula):
        assert self._is_formula(formula)
        truth = self.truth
        if isinstance(formula, AtomicFormula):
            return interpretation.symbol2truth[formula.symbol]
        elif isinstance(formula, Not):
            return not truth(interpretation, formula.f)
        elif isinstance(formula, And):
            return truth(interpretation, formula.f1) and truth(interpretation, formula.f2)
        elif isinstance(formula, Or):
            return truth(interpretation, formula.f1) or truth(interpretation, formula.f2)
        else:
            raise ValueError("Formula not recognized")
