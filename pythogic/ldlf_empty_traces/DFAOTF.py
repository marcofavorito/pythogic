"""DFA on the fly"""
from typing import List

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Formula import Formula, TrueFormula, FalseFormula, AtomicFormula, And
from pythogic.base.Symbol import Symbol
from pythogic.ldlf_empty_traces.LDLf_EmptyTraces import LDLf_EmptyTraces
from pythogic.pl.PL import PL


class DFAOTF(object):
    def __init__(self, ldlf:LDLf_EmptyTraces, f:Formula):
        assert ldlf.is_formula(f)
        self.ldlf = ldlf
        self.f = f
        self.reset()

    def reset(self):
        self.cur_state = frozenset([frozenset([self.f])])

    def trace_acceptance(self, action_set_list:List):
        self.reset()
        for a in action_set_list:
            self.make_transition(a)
        return self.is_true()

    def is_true(self):
        return frozenset() in self.cur_state

    def make_transition(self, actions_set):
        new_macrostate = set()
        for q in self.cur_state:
            delta_formulas = [self.ldlf.delta(subf, actions_set) for subf in q]
            atomics = [s for subf in delta_formulas for s in PL.find_atomics(subf)]

            symbol2formula = {Symbol(str(f)): f for f in atomics if f != TrueFormula() and f != FalseFormula()}
            formula2atomic_formulas = {
            f: AtomicFormula.fromName(str(f)) if f != TrueFormula() and f != FalseFormula() else f for f in atomics}
            transformed_delta_formulas = [self.ldlf._tranform_delta(f, formula2atomic_formulas) for f in delta_formulas]

            # the empy conjunction stands for true
            if len(transformed_delta_formulas) == 0:
                conjunctions = TrueFormula()
            else:
                conjunctions = And.chain(transformed_delta_formulas)

            models = frozenset(PL(Alphabet(set(symbol2formula))).minimal_models(conjunctions))
            if len(models) == 0:
                continue
            for min_model in models:
                q_prime = frozenset({symbol2formula[s] for s in min_model.symbol2truth if min_model.symbol2truth[s]})

                new_macrostate.add(q_prime)

        self.cur_state = frozenset(new_macrostate)
