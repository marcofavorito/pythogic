from typing import Set

from pythogic.ltlf.syntax.LTLfFormula import LTLfAtomicProposition, LTLfFormula, UnaryOperator, \
    BinaryOperator, DerivedLTLfFormula, LTLfTrue
from pythogic.misc.Symbol import DUMMY_SYMBOL


class LTLf(object):
    def __init__(self, propositions: Set[LTLfAtomicProposition]):
        assert len(propositions) > 0
        self.propositions = propositions

    def _is_formula(self, f: LTLfFormula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, LTLfAtomicProposition):
            return f in self.propositions or f == LTLfAtomicProposition(DUMMY_SYMBOL)
        elif isinstance(f, UnaryOperator):
            return self._is_formula(f.f)
        elif isinstance(f, BinaryOperator):
            return self._is_formula(f.f1) and self._is_formula(f.f2)
        elif isinstance(f, DerivedLTLfFormula):
            return self._is_formula(f._equivalent_formula())
        elif isinstance(f, LTLfTrue):
            return True
        else:
            raise ValueError("Argument not a valid Formula")
