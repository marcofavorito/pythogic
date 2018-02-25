from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.pl.PL import PL
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.base.Formula import AtomicFormula, Formula, Not, And, Or, PathExpressionFormula, PathExpressionUnion, \
    PathExpressionSequence, PathExpressionStar, PathExpressionTest, PathExpressionEventually, PathExpressionAlways, UnaryOperator, BinaryOperator, \
    PathExpression


class LDLf(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {AtomicFormula, Not, And, PathExpressionEventually}
    derived_formulas = {Or}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        # LDLfFormulas
        if isinstance(f, AtomicFormula):
            return True
        elif isinstance(f, UnaryOperator):
            return self.is_formula(f.f)
        elif isinstance(f, BinaryOperator):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, PathExpressionFormula):
            return self._is_path(f.p) and self.is_formula(f.f)
        else:
            raise ValueError("Argument not a valid Formula")

    def _is_path(self, p:PathExpression):
        # PathExpression
        if isinstance(p, Formula):
            pl = PL(self.alphabet)
            return pl.is_formula(p)
        elif isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return self._is_path(p.p1) and self._is_path(p.p2)
        elif isinstance(p, PathExpressionTest):
            return self.is_formula(p.f)
        elif isinstance(p, PathExpressionStar):
            return self._is_path(p.p)
        else:
            raise ValueError("Argument not a valid Path")

    def _is_testonly(self, p:PathExpression):
        if isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return self._is_testonly(p.p1) and self._is_testonly(p.p2)
        elif isinstance(p, PathExpressionStar):
            return self._is_testonly(p.p)
        else:
            return isinstance(p, PathExpressionTest)


    def _truth(self, f: Formula, trace: FiniteTrace, position: int):
        assert self._is_formula(f)
        assert trace.alphabet == self.alphabet
        truth = self._truth
        # LDLfFormulas
        if isinstance(f, AtomicFormula):
            return f in trace.get(position)
        elif isinstance(f, Not):
            return not self.truth(f.f, trace, position)
        elif isinstance(f, And):
            return self.truth(f.f1, trace, position) and self.truth(f.f2, trace, position)
        elif isinstance(f, Or):
            return self.truth(f.f1, trace, position) or self.truth(f.f2, trace, position)
        elif isinstance(f, PathExpressionEventually):
            path = f.p
            assert self._is_path(path)
            if isinstance(path, Formula):
                symbol2truth = {e: True if AtomicFormula(e) in trace.get(position) else False for e in self.alphabet.symbols}
                I = PLInterpretation(self.alphabet, symbol2truth)
                pl = PL(self.alphabet)
                return position < trace.last() and pl.truth(path, I)
            elif isinstance(path, PathExpressionTest):
                return truth(path.f, trace, position) and truth(f.f, trace, position)
            elif isinstance(path, PathExpressionUnion):
                return truth(PathExpressionEventually(path.p1, f.f), trace, position) or truth(PathExpressionEventually(path.p2, f.f), trace, position)
            elif isinstance(path, PathExpressionSequence):
                return truth(PathExpressionEventually(path.p1, PathExpressionEventually(path.p2, f.f)), trace, position)
            elif isinstance(path, PathExpressionStar):
                return truth(f.f, trace, position) or (
                    position<trace.last()
                    and truth(PathExpressionEventually(path.p, PathExpressionEventually(path, f.f)), trace, position)
                    and not self._is_testonly(path)
                )
        elif isinstance(f, PathExpressionAlways):
            return self.truth(Not(PathExpressionEventually(f.p, Not(f.f))), trace, position)
        else:
            raise ValueError("Argument not a valid Formula")
