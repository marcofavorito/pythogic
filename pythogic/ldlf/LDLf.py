from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.pl.PL import PL
from pythogic.base.Formula import AtomicFormula, Formula, Not, And, Or, PathExpressionFormula, PathExpressionUnion, \
    PathExpressionSequence, PathExpressionStar, PathExpressionTest, PathExpressionEventually, PathExpressionAlways, \
    PathExpression, FalseFormula, TrueFormula, LDLfLast, DUMMY_ATOMIC


class LDLf(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {AtomicFormula, Not, And, PathExpressionEventually}
    derived_formulas = {Or, PathExpressionAlways, TrueFormula, FalseFormula, LDLfLast}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        # LDLfFormulas
        if isinstance(f, AtomicFormula):
            return True
        elif isinstance(f, Not):
            return self.is_formula(f.f)
        elif isinstance(f, And):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, PathExpressionEventually):
            if isinstance(f.p, PathExpressionTest):
                return self.is_formula(f.f)
            else:
                return self._is_path(f.p) and self.is_formula(f.f)
        else:
            raise ValueError("Argument not a valid Formula")

    def _is_path(self, p: PathExpression):
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
    def _is_testonly(p: PathExpression):
        if isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return LDLf._is_testonly(p.p1) and LDLf._is_testonly(p.p2)
        elif isinstance(p, PathExpressionStar):
            return LDLf._is_testonly(p.p)
        else:
            return isinstance(p, PathExpressionTest)

    def _truth(self, f: Formula, trace: FiniteTrace, position: int):
        assert trace.alphabet == self.alphabet
        truth = self._truth
        # LDLfFormulas
        if isinstance(f, AtomicFormula):
            return f in trace.get(position)
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
                return truth(PathExpressionEventually(path.p1, f.f), trace, position) or truth(
                    PathExpressionEventually(path.p2, f.f), trace, position)
            elif isinstance(path, PathExpressionSequence):
                return truth(PathExpressionEventually(path.p1, PathExpressionEventually(path.p2, f.f)), trace, position)
            elif isinstance(path, PathExpressionStar):
                return truth(f.f, trace, position) or (
                    position < trace.last()
                    and truth(PathExpressionEventually(path.p, PathExpressionEventually(path, f.f)), trace, position)
                    and not self._is_testonly(path)
                )

            # Should be a Propositional Formula
            else:
                pl, I = PL._from_set_of_propositionals(trace.get(position), trace.alphabet)
                return position < trace.last() and pl.truth(path, I) and truth(f.f, trace, position + 1)
        else:
            raise ValueError("Argument not a valid Formula")

    def to_equivalent_formula(self, derived_formula: Formula):
        if isinstance(derived_formula, Or):
            return Not(And(Not(derived_formula.f1), Not(derived_formula.f2)))
        elif isinstance(derived_formula, PathExpressionAlways):
            return Not(PathExpressionEventually(derived_formula.p, Not(derived_formula.f)))
        elif isinstance(derived_formula, FalseFormula):
            return And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        elif isinstance(derived_formula, TrueFormula):
            return Not(FalseFormula())
        elif isinstance(derived_formula, LDLfLast):
            return PathExpressionAlways(TrueFormula(), FalseFormula())
        else:
            raise ValueError("Derived formula not recognized")

    def _expand_formula(self, f: Formula):
        if isinstance(f, AtomicFormula):
            return f
        elif isinstance(f, And):
            return And(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Not):
            return Not(self.expand_formula(f.f))
        elif isinstance(f, PathExpressionEventually):
            return PathExpressionEventually(f.p, self.expand_formula(f.f))
        else:
            raise ValueError("Not valid Formula to expand")

    def to_nnf(self, formula: Formula) -> Formula:
        if isinstance(formula, AtomicFormula):
            return formula
        elif isinstance(formula, And):
            return And(self.to_nnf(formula.f1), self.to_nnf(formula.f2))
        elif isinstance(formula, Or):
            return Or(self.to_nnf(formula.f1), self.to_nnf(formula.f2))
        elif isinstance(formula, PathExpressionFormula):
            return type(formula)(self.to_nnf_path(formula.p), self.to_nnf(formula.f))
        elif isinstance(formula, Not):
            return self._not_to_nnf(formula)
        else:
            raise ValueError

    def _not_to_nnf(self, not_formula: Not):
        subformula = not_formula.f
        if isinstance(subformula, AtomicFormula):
            return not_formula
        if isinstance(subformula, Not):
            # skip two consecutive Not
            new_formula = subformula.f
            return self.to_nnf(new_formula)
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
            return pl.to_nnf(path)
        else:
            raise ValueError

    # def compute_CL(self, formula: Formula) -> Set[Formula]:
    #     old = set()
    #     new = {formula}
    #     while old != new:
    #         old = old.union(new)
    #
    #         for f in old:
    #             if isinstance(f, AtomicFormula):
    #                 new.add(f)
    #             elif isinstance(f, And) or isinstance(f, Or):
    #                 new.add(f.f1)
    #                 new.add(f.f2)
    #             elif isinstance(f, Not):
    #                 if not isinstance(f.f, Not) and f.f in old:
    #                     new.add(f.f)
    #             elif isinstance(f, PathExpressionEventually):
    #                 new.add(f.f)
    #                 if isinstance(f.p, PathExpressionTest):
    #                     new.add(f.p.f)
    #                 elif isinstance(f.p, PathExpressionSequence):
    #                     new.add(PathExpressionEventually(f.p.p1, PathExpressionEventually(f.p.p2, f.f)))
    #                 elif isinstance(f.p, PathExpressionUnion):
    #                     new.add(PathExpressionEventually(f.p.p1, f.f))
    #                     new.add(PathExpressionEventually(f.p.p2, f.f))
    #                 elif isinstance(f.p, PathExpressionStar):
    #                     new.add(PathExpressionEventually(f.p.p, PathExpressionEventually(f.p, f.f)))
    #                 elif isinstance(f.p, Formula):
    #                     new.add(f.p)
    #                 else:
    #                     raise ValueError
    #
    #     return old
    #
    # def to_nfa(self, f: Formula) -> dict:
    #     nnf_f = self.to_nnf(f)
    #     alphabet = powerset(self.alphabet.symbols)
    #     states = self.compute_CL(nnf_f)
    #     initial_state = nnf_f
    #     final_states = {}
    #     delta = {}
    #     for action in alphabet:
    #         action_set = set(action)
    #         for s in states:
    #             delta[(s, action)] = self._compute_delta(s, action_set)
    #     return {
    #         "alphabet": alphabet,
    #         "states": states,
    #         "initial_state": initial_state,
    #         "delta": delta,
    #         "final_state": final_states
    #     }
    #
    # def _compute_delta(self, s, action: Set[Symbol]):
    #     if isinstance(s, AtomicFormula):
    #         return s.symbol in action
    #     elif isinstance(s, And):
    #         return self._compute_delta(s.f1, action) and self._compute_delta(s.f2, action)
    #     elif isinstance(s, Or):
    #         return self._compute_delta(s.f1, action) or self._compute_delta(s.f2, action)
    #     elif isinstance(s, PathExpressionEventually):
    #         if isinstance(s.p, PathExpressionTest):
    #             self._compute_delta(s.p, action) and self._compute_delta(s.f, action)
    #         elif isinstance(s.p, PathExpressionSequence):
    #             return self._compute_delta(PathExpressionEventually(s.p.p1, PathExpressionEventually(s.p.p2, s.f)),
    #                                        action)
    #         elif isinstance(s.p, PathExpressionUnion):
    #             return self._compute_delta(PathExpressionEventually(s.p.p1, s.f), action) or self._compute_delta(
    #                 PathExpressionEventually(s.p.p2, s.f), action)
    #         elif isinstance(s.p, PathExpressionStar):
    #             if LDLf._is_testonly(s.p.p):
    #                 return self._compute_delta(s.f, action)
    #             else:
    #                 return self._compute_delta(s.f, action) or self._compute_delta(PathExpressionEventually(s.p.p, s),
    #                                                                                action)
    #         elif isinstance(s.p, Formula):
    #             pl, I = PL._from_set_of_propositionals(action, self.alphabet)
    #             if pl.truth(s.p, I):
    #                 return s.f
    #             else:
    #                 return False
    #     elif isinstance(s, PathExpressionAlways):
    #         if isinstance(s.p, PathExpressionTest):
    #             self._compute_delta(self.to_nnf(Not(s.p.f)), action) or self._compute_delta(s.f, action)
    #         elif isinstance(s.p, PathExpressionSequence):
    #             return self._compute_delta(PathExpressionAlways(s.p.p1, PathExpressionAlways(s.p.p2, s.f)), action)
    #         elif isinstance(s.p, PathExpressionUnion):
    #             return self._compute_delta(PathExpressionAlways(s.p.p1, s.f), action) and self._compute_delta(
    #                 PathExpressionAlways(s.p.p2, s.f), action)
    #         elif isinstance(s.p, PathExpressionStar):
    #             if LDLf._is_testonly(s.p.p):
    #                 return self._compute_delta(s.f, action)
    #             else:
    #                 return self._compute_delta(s.f, action) and self._compute_delta(PathExpressionEventually(s.p.p, s),
    #                                                                                 action)
    #         elif isinstance(s.p, Formula):
    #             pl, I = PL._from_set_of_propositionals(action, self.alphabet)
    #             if pl.truth(s.p, I):
    #                 return s.f
    #             else:
    #                 return True
