from typing import Set

from pythogic.ltlf.syntax.LTLfFormula import LTLfAtomicProposition, LTLfFormula, UnaryOperator, \
    BinaryOperator


class LTLf(object):
    def __init__(self, propositions: Set[LTLfAtomicProposition]):
        self.propositions = propositions

    def _is_formula(self, f: LTLfFormula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, LTLfAtomicProposition):
            return f in self.propositions
        elif isinstance(f, UnaryOperator):
            return self._is_formula(f.f)
        elif isinstance(f, BinaryOperator):
            return self._is_formula(f.f1) and self._is_formula(f.f2)
        else:
            raise ValueError("Argument not a valid Formula")
