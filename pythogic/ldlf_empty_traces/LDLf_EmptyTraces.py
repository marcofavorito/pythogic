from typing import Set, FrozenSet

from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.base.Formula import Formula, Not, And, Or, PathExpressionFormula, PathExpressionUnion, \
    PathExpressionSequence, PathExpressionStar, PathExpressionTest, PathExpressionEventually, PathExpressionAlways, \
    PathExpression, FalseFormula, TrueFormula, LDLfLast, DUMMY_ATOMIC, LogicalTrue, LogicalFalse, Until, Next, End, \
    AtomicFormula
from pythogic.base.Symbol import Symbol
from pythogic.base.utils import powerset
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.pl.PL import PL


class F(Formula):
    def __init__(self, f: Formula):
        self.f = f

    def _members(self):
        return ("F", self.f)

    def __str__(self):
        return "_".join(map(str,self._members()))





class T(Formula):
    def __init__(self, f: Formula):
        self.f = f

    def _members(self):
        return ("T", self.f)

    def __str__(self):
        return "_".join(map(str,self._members()))



class LDLf_EmptyTraces(FormalSystem):



    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)
        self.pl = PL(self.alphabet)

    allowed_formulas = {LogicalTrue, Not, And, PathExpressionEventually, TrueFormula, FalseFormula}
    derived_formulas = {LogicalFalse, Or, Next, Until, End, PathExpressionAlways, LDLfLast, AtomicFormula}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        # Check first if it is a propositional
        pl = PL(self.alphabet)
        if pl.is_formula(f):
            return self.is_formula(PathExpressionEventually(f, LogicalTrue()))
        elif isinstance(f, LogicalTrue):
            return True
        elif isinstance(f, Not):
            return self.is_formula(f.f)
        elif isinstance(f, And):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, PathExpressionEventually):
            return self._is_path(f.p) and self.is_formula(f.f)
        else:
            return False

    def _is_path(self, p: PathExpression):
        # PathExpression
        if isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return self._is_path(p.p1) and self._is_path(p.p2)
        elif isinstance(p, PathExpressionTest):
            if self.pl.is_formula(p.f):
                return True
            else:
                return self.is_formula(p.f)
        elif isinstance(p, PathExpressionStar):
            return self._is_path(p.p)
        elif isinstance(p, Formula):
            pl = PL(self.alphabet)
            return pl.is_formula(p)
        else:
            raise ValueError("Argument not a valid Path")

    def expand_formula(self, f:Formula):
        """Manage the case when we have a propositional formula."""
        # Check first if it is a propositional
        pl = PL(self.alphabet)
        if pl.is_formula(f):
            return super().expand_formula(PathExpressionEventually(f, LogicalTrue()))
        else:
            return super().expand_formula(f)


    def _expand_formula(self, f: Formula):
        if isinstance(f, LogicalTrue):
            return f
        elif isinstance(f, And):
            return And(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Not):
            return Not(self.expand_formula(f.f))
        elif isinstance(f, PathExpressionEventually):
            return PathExpressionEventually(self._expand_path(f.p), self.expand_formula(f.f))
        else:
            raise ValueError("Not valid Formula to expand")

    def _expand_path(self, p:PathExpression) -> PathExpression:
        if isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return type(p)(self._expand_path(p.p1), self._expand_path(p.p2))
        elif isinstance(p, PathExpressionTest):
            return PathExpressionTest(self.expand_formula(p.f))
        elif isinstance(p, PathExpressionStar):
            return PathExpressionStar(self._expand_path(p.p))
        elif isinstance(p, Formula):
            pl = PL(self.alphabet)
            return pl.expand_formula(p)
        else:
            raise ValueError

    @staticmethod
    def _is_testonly(p: PathExpression):
        if isinstance(p, PathExpressionUnion) or isinstance(p, PathExpressionSequence):
            return LDLf_EmptyTraces._is_testonly(p.p1) and LDLf_EmptyTraces._is_testonly(p.p2)
        elif isinstance(p, PathExpressionStar):
            return LDLf_EmptyTraces._is_testonly(p.p)
        else:
            return isinstance(p, PathExpressionTest)

    def _truth(self, f: Formula, trace: FiniteTrace, position: int):
        assert trace.alphabet == self.alphabet
        truth = self._truth

        pl = PL(self.alphabet)
        if pl.is_formula(f):
            return self.truth(PathExpressionEventually(f, LogicalTrue()), trace, position)
        elif isinstance(f, LogicalTrue):
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
            # path should be a Propositional Formula
            else:
                pl, I = PL._from_set_of_propositionals(trace.get(position), trace.alphabet)
                return position < trace.length() and pl.truth(path, I) and truth(f.f, trace, position + 1)
        else:
            raise ValueError("Argument not a valid Formula")

    def to_equivalent_formula(self, derived_formula: Formula):
        # make lines shorter
        ef = self.to_equivalent_formula
        if isinstance(derived_formula, AtomicFormula):
            return PathExpressionEventually(derived_formula, LogicalTrue())
        elif isinstance(derived_formula, LogicalFalse):
            return Not(LogicalTrue())
        elif isinstance(derived_formula, Or):
            return Not(And(Not(derived_formula.f1), Not(derived_formula.f2)))
        elif isinstance(derived_formula, PathExpressionAlways):
            return Not(PathExpressionEventually(derived_formula.p, Not(derived_formula.f)))
        elif isinstance(derived_formula, Next):
            return PathExpressionEventually(TrueFormula(), And(derived_formula.f, Not(ef(End()))))
        elif isinstance(derived_formula, End):
            return ef(PathExpressionAlways(TrueFormula(), ef(LogicalFalse())))
        elif isinstance(derived_formula, Until):
            return PathExpressionEventually(
                PathExpressionStar(PathExpressionSequence(PathExpressionTest(derived_formula.f1), ef(TrueFormula()))),
                And(derived_formula.f2, Not(ef(End())))
            )
        elif isinstance(derived_formula, FalseFormula):
            return FalseFormula()
        elif isinstance(derived_formula, TrueFormula):
            return TrueFormula()
        elif isinstance(derived_formula, LDLfLast):
            return PathExpressionEventually(ef(TrueFormula()), ef(End()))
        # propositional
        elif isinstance(derived_formula, Formula):
            pl = PL(self.alphabet)
            assert pl.is_formula(derived_formula)
            f = pl.to_nnf(derived_formula)
            return PathExpressionEventually(f, LogicalTrue())
        else:
            raise ValueError("Derived formula not recognized")

    def to_nnf(self, f: Formula) -> Formula:
        formula = self.expand_formula(f)
        pl = PL(self.alphabet)
        if pl.is_formula(formula):
            return pl.to_nnf(formula)
        elif isinstance(formula, LogicalTrue):
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
        elif isinstance(subformula, LogicalTrue):
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
            if pl.is_formula(path):
                return pl.to_nnf(path)
            else:
                raise ValueError
        else:
            raise ValueError


    def to_nfa(self, f:Formula):
        # TODO: optimize!!!
        assert self.is_formula(f)
        nnf_f = self.to_nnf(f)

        alphabet = powerset(self.alphabet.symbols)
        initial_states = {frozenset([nnf_f])}
        final_states = {frozenset()}
        delta = set()

        pl, I = PL._from_set_of_propositionals(set(), Alphabet(set()))
        d = self.delta(nnf_f, frozenset(), epsilon=True)
        if pl.truth(d, I):
            final_states.add(frozenset([nnf_f]))

        states = {frozenset(), frozenset([nnf_f])}

        states_changed, delta_changed = True, True
        while states_changed or delta_changed:

            states_changed, delta_changed = False, False
            for actions_set in alphabet:
                states_list = list(states)
                for q in states_list:

                    delta_formulas = [self.delta(subf, actions_set) for subf in q]
                    atomics = [s for subf in delta_formulas for s in PL.find_atomics(subf)]

                    symbol2formula = {Symbol(str(f)) : f for f in atomics if f != TrueFormula() and f!=FalseFormula()}
                    formula2atomic_formulas = {f : AtomicFormula.fromName(str(f)) if f != TrueFormula() and f!=FalseFormula() else f for f in atomics}
                    transformed_delta_formulas = [self._tranform_delta(f, formula2atomic_formulas) for f in delta_formulas]
                    conjunctions = And.chain(transformed_delta_formulas)

                    models = frozenset(PL(Alphabet(set(symbol2formula))).minimal_models(conjunctions))
                    if len(models)==0:
                        continue
                    for min_model in models:
                        q_prime = frozenset({symbol2formula[s] for s in min_model.symbol2truth if min_model.symbol2truth[s]})


                        len_before = len(states)
                        states.add(q_prime)
                        if len(states) == len_before + 1:
                            states_list.append(q_prime)
                            states_changed = True

                        len_before = len(delta)
                        delta.add((q, actions_set, q_prime))
                        if len(delta) == len_before + 1:
                            delta_changed = True

                        # check if q_prime should be added as final state
                        if len(q_prime) == 0:
                            final_states.add(q_prime)
                        else:
                            q_prime_delta_conjunction = And.chain([self.delta(subf, frozenset(), epsilon=True) for subf in q_prime])
                            pl, I = PL._from_set_of_propositionals(set(), Alphabet(set()))
                            if pl.truth(q_prime_delta_conjunction, I):
                                final_states.add(q_prime)

        return {
            "alphabet": alphabet,
            "states": frozenset(states),
            "initial_states": frozenset(initial_states),
            "transitions": delta,
            "accepting_states": frozenset(final_states)
        }



    def _tranform_delta(self, f:Formula, formula2AtomicFormula):
        if isinstance(f, Not):
            return Not(self._tranform_delta(f, formula2AtomicFormula))
        elif isinstance(f, And) or isinstance(f, Or):
            return type(f)(self._tranform_delta(f.f1, formula2AtomicFormula), self._tranform_delta(f.f2, formula2AtomicFormula))
        elif isinstance(f, TrueFormula) or isinstance(f, FalseFormula):
            return f
        else:
            return formula2AtomicFormula[f]


    def delta(self, f:Formula, action: FrozenSet[Symbol], epsilon=False):
        # TODO: should return [True|False]Formula or simply True/False?
        pl, I = PL._from_set_of_propositionals(action, self.alphabet)
        if pl.is_formula(f):
            return self.delta(PathExpressionEventually(f, LogicalTrue()), action, epsilon)
        elif isinstance(f, LogicalTrue):
            return TrueFormula()
        elif isinstance(f, LogicalFalse):
            return FalseFormula()
        elif isinstance(f, And):
            return And(self.delta(f.f1, action), self.delta(f.f2, action, epsilon))
        elif isinstance(f, Or):
            return Or(self.delta(f.f1, action), self.delta(f.f2, action, epsilon))
        elif isinstance(f, PathExpressionEventually):
            if pl.is_formula(f.p):
                if not epsilon and pl.truth(f.p, I):
                    return self._expand(f.f)
                else:
                    return FalseFormula()
            elif isinstance(f.p, PathExpressionTest):
                return And(self.delta(f.p.f, action, epsilon), self.delta(f.f, action, epsilon))
            elif isinstance(f.p, PathExpressionUnion):
                return Or(self.delta(PathExpressionEventually(f.p.p1, f.f), action, epsilon),
                       self.delta(PathExpressionEventually(f.p.p2, f.f), action, epsilon))
            elif isinstance(f.p, PathExpressionSequence):
                e2 = PathExpressionEventually(f.p.p2, f.f)
                e1 = PathExpressionEventually(f.p.p1, e2)
                return self.delta(e1, action, epsilon)
            elif isinstance(f.p, PathExpressionStar):
                o1 = self.delta(f.f, action, epsilon)
                o2 = self.delta(PathExpressionEventually(f.p.p, F(f)), action, epsilon)
                return Or(o1, o2)
        elif isinstance(f, PathExpressionAlways):
            if pl.is_formula(f.p):
                if not epsilon and pl.truth(f.p, I):
                    return self._expand(f.f)
                else:
                    return TrueFormula()
            elif isinstance(f.p, PathExpressionTest):
                o1 = self.delta(self.to_nnf(Not(f.p.f)), action, epsilon)
                o2 = self.delta(f.f, action, epsilon)
                return Or(o1, o2)
            elif isinstance(f.p, PathExpressionUnion):
                return And(self.delta(PathExpressionAlways(f.p.p1, f.f), action, epsilon),
                       self.delta(PathExpressionAlways(f.p.p2, f.f), action, epsilon))
            elif isinstance(f.p, PathExpressionSequence):
                return self.delta(PathExpressionAlways(f.p.p1, PathExpressionAlways(f.p.p2, f.f)), action, epsilon)
            elif isinstance(f.p, PathExpressionStar):
                a1 = self.delta(f.f, action, epsilon)
                a2 = self.delta(PathExpressionAlways(f.p.p, T(f)), action, epsilon)
                return And(a1, a2)
        elif isinstance(f, F):
            return FalseFormula()
        elif isinstance(f, T):
            return TrueFormula()
        else:
            raise ValueError


    def _expand(self, f:Formula):
        if isinstance(f, F) or isinstance(f, T):
            return self._expand(f.f)
        elif isinstance(f, PathExpressionEventually) or isinstance(f, PathExpressionAlways):
            return type(f)(f.p, self._expand(f.f))
        else:
            return f


