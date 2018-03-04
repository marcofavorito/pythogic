from typing import Set

from pythogic.base.Symbol import Symbol
from pythogic.base.utils import powerset
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.pl.PL import PL
from pythogic.base.Formula import AtomicFormula, Formula, Not, And, Or, PathExpressionFormula, PathExpressionUnion, \
    PathExpressionSequence, PathExpressionStar, PathExpressionTest, PathExpressionEventually, PathExpressionAlways, \
    UnaryOperator, BinaryOperator, \
    PathExpression, FalseFormula, TrueFormula, LDLfLast, DUMMY_ATOMIC, LogicalTrue, LogicalFalse, Until, Next, End


class LDLf_EmptyTraces(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {LogicalTrue, Not, And, PathExpressionEventually}
    derived_formulas = {LogicalFalse, Or, Next, Until, End, PathExpressionAlways, TrueFormula, FalseFormula, LDLfLast}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        # LDLfFormulas
        if isinstance(f, LogicalTrue):
            return True
        elif isinstance(f, Not):
            return self.is_formula(f.f)
        elif isinstance(f, And):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, PathExpressionEventually):
            return self._is_path(f.p) and self.is_formula(f.f)
        else:
            raise ValueError("Argument not a valid Formula")

    def _is_path(self, p:PathExpression):
        # PathExpression
        if isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return self._is_path(p.p1) and self._is_path(p.p2)
        elif isinstance(p, PathExpressionTest):
            return self.is_formula(p.f)
        elif isinstance(p, PathExpressionStar):
            return self._is_path(p.p)
        elif isinstance(p, Formula):
            pl = PL(self.alphabet)
            return pl.is_formula(p)
        else:
            raise ValueError("Argument not a valid Path")

    @staticmethod
    def _is_testonly(p:PathExpression):
        if isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return LDLf_EmptyTraces._is_testonly(p.p1) and LDLf_EmptyTraces._is_testonly(p.p2)
        elif isinstance(p, PathExpressionStar):
            return LDLf_EmptyTraces._is_testonly(p.p)
        else:
            return isinstance(p, PathExpressionTest)


    def _truth(self, f: Formula, trace: FiniteTrace, position: int):
        assert trace.alphabet == self.alphabet
        truth = self._truth
        # LDLfFormulas
        if isinstance(f, LogicalTrue):
            return True
        elif isinstance(f, Not):
            return not self.truth(f.f, trace, position)
        elif isinstance(f, And):
            return self.truth(f.f1, trace, position) and self.truth(f.f2, trace, position)
        elif isinstance(f, PathExpressionEventually):
            path = f.p
            assert self._is_path(path)
            if isinstance(path, PathExpressionTest):
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
            # It is a Propositional Formula, maybe...
            elif isinstance(path, Formula):
                pl, I = PL._from_set_of_propositionals(trace.get(position), trace.alphabet)
                assert pl.is_formula(path)
                return position < trace.last() and pl.truth(path, I) and truth(f.f, trace, position+1)
        else:
            raise ValueError("Argument not a valid Formula")

    def to_equivalent_formula(self, derived_formula:Formula):
        if isinstance(derived_formula, LogicalFalse):
            return Not(LogicalTrue())
        elif isinstance(derived_formula, Or):
            return Not(And(Not(derived_formula.f1), Not(derived_formula.f2)))
        elif isinstance(derived_formula, PathExpressionAlways):
            return Not(PathExpressionEventually(derived_formula.p, Not(derived_formula.f)))
        elif isinstance(derived_formula, Next):
            return PathExpressionEventually(TrueFormula(), And(derived_formula.f, Not(End())))
        elif isinstance(derived_formula, End):
            return PathExpressionAlways(TrueFormula(), LogicalFalse())
        elif isinstance(derived_formula, PathExpressionAlways):
            return Not(PathExpressionEventually(derived_formula.p, Not(derived_formula.f)))
        elif isinstance(derived_formula, Until):
            return PathExpressionEventually(
                PathExpressionStar(PathExpressionSequence(PathExpressionTest(derived_formula.f1),TrueFormula())),
                And(derived_formula.f2, Not(End()))
            )
        elif isinstance(derived_formula, FalseFormula):
            return And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        elif isinstance(derived_formula, TrueFormula):
            return Not(FalseFormula())
        elif isinstance(derived_formula, LDLfLast):
            return PathExpressionEventually (TrueFormula(), End())
        elif isinstance(derived_formula, Formula):
            # Check if it is a Propositional Formula
            pl = PL(self.alphabet)
            return pl.is_formula(derived_formula)
        else:
            raise ValueError("Derived formula not recognized")



    def to_nnf(self, formula:Formula)->Formula:
        if isinstance(formula, LogicalTrue):
            return formula
        elif isinstance(formula, And):
            return And(self.to_nnf(formula.f1), self.to_nnf(formula.f2))
        elif isinstance(formula, PathExpressionFormula):
            return type(formula)(self.to_nnf_path(formula.p), self.to_nnf(formula.f))
        elif isinstance(formula, Not):
            return self._not_to_nnf(formula)
        else:
            raise ValueError

    def _not_to_nnf(self, not_formula: Not):
        subformula = not_formula.f
        if isinstance(subformula, Not):
            # skip two consecutive Not
            new_formula = subformula.f
            return self.to_nnf(new_formula)
        elif isinstance(subformula, LogicalTrue()):
            return LogicalFalse()
        elif isinstance(subformula, And):
            return Or(self.to_nnf(Not(subformula.f1)), self.to_nnf(Not(subformula.f2)))
        elif isinstance(subformula, Or):
            return And(self.to_nnf(Not(subformula.f1)), self.to_nnf(Not(subformula.f2)))
        elif isinstance(subformula, PathExpressionEventually):
            return PathExpressionAlways(self.to_nnf_path(subformula.p), self.to_nnf(Not(subformula.f)))
        elif isinstance(subformula, PathExpressionAlways):
            return PathExpressionEventually(self.to_nnf_path(subformula.p), self.to_nnf(Not(subformula.f)))
        else:
            raise ValueError


    def to_nnf_path(self, path: PathExpression):
        if isinstance(path, PathExpressionTest):
            return PathExpressionTest(self.to_nnf(path.f))
        elif isinstance(path, PathExpressionUnion):
            return PathExpressionUnion(self.to_nnf_path(path.p1), self.to_nnf_path(path.p2))
        elif isinstance(path, PathExpressionSequence):
            return PathExpressionSequence(self.to_nnf_path(path.p1), self.to_nnf_path(path.p2))
        elif isinstance(path, PathExpressionStar):
            return PathExpressionStar(self.to_nnf_path(path.p))
        elif isinstance(path, Formula):
            pl = PL(self.alphabet)
            assert pl.is_formula(path)
            return path
        else:
            raise ValueError