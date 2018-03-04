from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.base.Formula import PathExpressionUnion, PathExpressionStar, PathExpressionSequence, Formula, \
    PathExpressionTest
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.pl.PL import PL


class REf(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {PathExpressionUnion, PathExpressionSequence, PathExpressionStar}
    derived_formulas = {}


    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, PathExpressionUnion):
            return self.is_formula(f.p1) and self.is_formula(f.p2)
        elif isinstance(f, PathExpressionSequence):
            return self._is_formula(f.p1) and self._is_formula(f.p2)
        elif isinstance(f, PathExpressionStar):
            return self._is_formula(f.p)
        else:
            pl = PL(self.alphabet)
            return pl.is_formula(f)

    def _truth(self, f: Formula, trace: FiniteTrace, start: int, end:int):
        assert self._is_formula(f)
        assert trace.alphabet == self.alphabet
        truth = self.truth
        if isinstance(f, PathExpressionUnion):
            return truth(f.p1, trace, start, end) or truth(f.p2, trace, start, end)
        if isinstance(f, PathExpressionSequence):
            return any(truth(f.p1, trace, start, k) and truth(f.p2, trace, k, end) for k in range(start, end+1))
        if isinstance(f, PathExpressionStar):
            return end == start or any(truth(f.p, trace, start, k) and truth(f, trace, k, end) for k in range(start, end + 1))
        else:
            pl, I = PL._from_set_of_propositionals(trace.get(start), self.alphabet)
            assert pl.is_formula(f)
            return end == start+1 and end <= trace.length() and pl.truth(f, I)

    def to_nnf(self, f:Formula):
        if isinstance(f, PathExpressionUnion):
            return PathExpressionUnion(self.to_nnf(f.p1), self.to_nnf(f.p2))
        elif isinstance(f, PathExpressionSequence):
            return PathExpressionSequence(self.to_nnf(f.p1), self.to_nnf(f.p2))
        elif isinstance(f, PathExpressionStar):
            return PathExpressionStar(self.to_nnf(f.p))
        elif isinstance(f, Formula):
            pl = PL(self.alphabet)
            assert pl.is_formula(f)
            return f
        else:
            raise ValueError

    def to_equivalent_formula(self, derived_formula: Formula):
        raise NotImplementedError

    def _expand_formula(self, f: Formula):
        raise NotImplementedError
