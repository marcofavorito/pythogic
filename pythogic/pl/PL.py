"""Propositional Logic"""
from typing import Set

from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.base.Symbol import DUMMY_SYMBOL, Symbol
from pythogic.base.utils import powerset
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.base.Formula import AtomicFormula, TrueFormula, FalseFormula, Formula, Not, Or, And, Implies, \
    DUMMY_ATOMIC, Equivalence


class PL(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {AtomicFormula, Not, And, TrueFormula, FalseFormula}
    derived_formulas = {Or, Implies, Equivalence}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, AtomicFormula):
            a = f.symbol in self.alphabet.symbols
            return f.symbol in self.alphabet.symbols or f.symbol == DUMMY_SYMBOL
        elif isinstance(f, Not):
            return self.is_formula(f.f)
        elif isinstance(f, And):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, TrueFormula) or isinstance(f, FalseFormula):
            return f
        else:
            return False

    def _truth(self, formula: Formula, interpretation: PLInterpretation):
        assert self._is_formula(formula)
        truth = self.truth
        if isinstance(formula, AtomicFormula):
            try:
                return interpretation.symbol2truth[formula.symbol]
            except:
                return False
        elif isinstance(formula, FalseFormula):
            return False
        elif isinstance(formula, TrueFormula):
            return True
        elif isinstance(formula, Not):
            return not truth(formula.f, interpretation)
        elif isinstance(formula, And):
            return truth(formula.f1, interpretation) and truth(formula.f2, interpretation)
        else:
            raise ValueError("Formula not recognized")

    def to_equivalent_formula(self, derived_formula:Formula):
        if isinstance(derived_formula, Or):
            return Not(And(Not(derived_formula.f1), Not(derived_formula.f2)))
        elif isinstance(derived_formula, Implies):
            return Not(And(derived_formula.f1, Not(derived_formula.f2)))
        elif isinstance(derived_formula, Equivalence):
            positive_equivalence = And(derived_formula.f1, derived_formula.f2)
            negative_equivalence = And(Not(derived_formula.f1), Not(derived_formula.f2))
            return Not(And(Not(positive_equivalence), Not(negative_equivalence)))
        elif derived_formula in PL.allowed_formulas:
            return derived_formula
        else:
            raise ValueError("Derived formula not recognized")

    def _expand_formula(self, f:Formula):
        if isinstance(f, AtomicFormula):
            return f
        elif isinstance(f, And):
            return And(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Not):
            return Not(self.expand_formula(f.f))
        elif type(f) in self.derived_formulas:
            return self.expand_formula(self.to_equivalent_formula(f))
        elif isinstance(f, FalseFormula):
            return FalseFormula()
        elif isinstance(f, TrueFormula):
            return TrueFormula()
        else:
            raise ValueError("Formula to expand not recognized")

    @staticmethod
    def _from_set_of_propositionals(props:Set[Symbol], alphabet:Alphabet):
        symbol2truth = {e: True if e in props else False for e in alphabet.symbols}
        I = PLInterpretation(alphabet, symbol2truth)
        pl = PL(alphabet)
        return pl, I


    def to_nnf(self, f:Formula):
        assert self.is_formula(f)
        formula = self.expand_formula(f)
        # formula = f
        if isinstance(formula, AtomicFormula) or isinstance(formula, TrueFormula) or isinstance(formula, FalseFormula):
            return formula
        elif isinstance(formula, And):
            return And(self.to_nnf(formula.f1), self.to_nnf(formula.f2))
        elif isinstance(formula, Not):
            subformula = formula.f
            if isinstance(subformula, Not):
                return self.to_nnf(subformula.f)
            elif isinstance(subformula, And):
                return Or(self.to_nnf(Not(subformula.f1)), self.to_nnf((Not(subformula.f2))))
            elif isinstance(subformula, AtomicFormula):
                return formula
            else:
                raise ValueError
        else:
            raise ValueError

    @staticmethod
    def find_atomics(formula:Formula)-> Set[AtomicFormula]:
        pl = PL(Alphabet(set()))
        f = formula
        res = set()
        if isinstance(f, TrueFormula) or isinstance(f, FalseFormula):
            res.add(f)
        elif isinstance(f, AtomicFormula):
            res.add(f)
        elif isinstance(f, Not):
            res = res.union(PL.find_atomics(f.f))
        elif isinstance(f, And) or isinstance(f, Or):
            res = res.union(PL.find_atomics(f.f1)).union(PL.find_atomics(f.f2))
        else:
            res.add(f)
        return res


    def minimal_models(self, f:Formula)-> Set[PLInterpretation]:
        """Find models of min size (i.e. the less number of proposition to True).
        Very trivial (and inefficient) algorithm: BRUTE FORCE on sorted-by-size interpretations
        """
        all_possible_interpretations = sorted(powerset(self.alphabet.symbols), key=len)
        size2models = {}
        for i in all_possible_interpretations:
            # compute current Interpretation, considering False
            # all propositional symbols not present in current interpretation
            current_interpretation = PLInterpretation(self.alphabet, {s: s in i for s in self.alphabet.symbols})
            if self.truth(f, current_interpretation):
                if not len(i) in size2models:
                    size2models[len(i)] = set()
                size2models[len(i)].add(current_interpretation)

        if not size2models:
            return set()
        else:
            return size2models[min(size2models.keys())]
