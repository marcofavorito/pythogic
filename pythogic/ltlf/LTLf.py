
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.ltlf.syntax.LTLfFormula import LTLfAtomicProposition, LTLfFormula, UnaryOperator, \
    BinaryOperator, DerivedLTLfFormula, LTLfTrue, Not, And, Next, Until
from pythogic.misc.Alphabet import Alphabet
from pythogic.misc.FormalSystem import FormalSystem
from pythogic.misc.Symbol import DUMMY_SYMBOL


class LTLf(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    def _is_formula(self, f: LTLfFormula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, LTLfAtomicProposition):
            return f.symbol in self.alphabet.symbols or f == LTLfAtomicProposition(DUMMY_SYMBOL)
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

    def truth(self, trace: FiniteTrace, position: int, formula: LTLfFormula):
        assert self._is_formula(formula)
        truth = self.truth
        if isinstance(formula, LTLfAtomicProposition):
            return formula in trace.get(position)
        elif isinstance(formula, Not):
            return not truth(trace, position, formula.f)
        elif isinstance(formula, And):
            return truth(trace, position, formula.f1) and truth(trace, position, formula.f2)
        elif isinstance(formula, Next):
            return position < trace.last() and truth(trace, position + 1, formula.f)
        elif isinstance(formula, Until):
            return any(
                truth(trace, j, formula.f2)
                and all(
                    truth(trace, k, formula.f1) for k in range(position, j)
                )
                for j in range(position, trace.last() + 1)
            )
        elif isinstance(formula, DerivedLTLfFormula):
            return truth(trace, position, formula._equivalent_formula())
        else:
            raise ValueError("Not valid formula")
