"""Propositional Logic"""
from typing import Set

from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.base.Symbol import DUMMY_SYMBOL, Symbol
from pythogic.base.utils import powerset
from pythogic.pl import PLutils
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.base.Formula import AtomicFormula, TrueFormula, FalseFormula, Formula, Not, Or, And, Implies, \
    DUMMY_ATOMIC, Equivalence


class PropositionalFormula(Formula):
    def __init__(self, f:Formula):
        self.f = f

    def _members(self):
        return self.f._members()

    def __str__(self):
        return self.f.__str__()

class PL(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {AtomicFormula, Not, And}
    derived_formulas = {
        Or:           PLutils._or_to_and,
        Implies:      PLutils._implies_to_or,
        Equivalence:  PLutils._equivalence_to_equivalent_formula,
        TrueFormula:  PLutils._trueFormula_to_equivalent_formula,
        FalseFormula: PLutils._falseFormula_to_equivalent_formula
    }

    def getPropositionalFormula(self, f:Formula):
        if self.is_formula(f):
            return PropositionalFormula(f)
        else:
            raise ValueError

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

    def expand_formula(self, f: Formula):
        if isinstance(f, TrueFormula) or isinstance(f, FalseFormula):
            return f
        else:
            return super().expand_formula(f)

    def _expand_formula(self, f:Formula):
        if isinstance(f, AtomicFormula):
            return f
        elif isinstance(f, And):
            return And(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Not):
            return Not(self.expand_formula(f.f))
        else:
            raise ValueError("Formula to expand not recognized")

    @staticmethod
    def _from_set_of_propositionals(props:Set[Symbol], alphabet:Alphabet):
        symbol2truth = {e: True if e in props else False for e in alphabet.symbols}
        I = PLInterpretation(alphabet, symbol2truth)
        pl = PL(alphabet)
        return pl, I


    def to_nnf(self, f:Formula):
        # assert self.is_formula(f)
        # formula = self.expand_formula(f)
        formula = f
        if isinstance(formula, AtomicFormula) or isinstance(formula, TrueFormula) or isinstance(formula, FalseFormula):
            return formula
        elif isinstance(formula, And) or isinstance(formula, Or):
            return type(formula)(self.to_nnf(formula.f1), self.to_nnf(formula.f2))
        elif type(formula) in self.derived_formulas:
            return self.to_nnf(self.derived_formulas[type(formula)](formula))
        elif isinstance(formula, Not):
            subformula = formula.f
            if isinstance(subformula, Not):
                return self.to_nnf(subformula.f)
            elif isinstance(subformula, And):
                return Or(self.to_nnf(Not(subformula.f1)), self.to_nnf((Not(subformula.f2))))
            elif isinstance(subformula, Or):
                return And(self.to_nnf(Not(subformula.f1)), self.to_nnf((Not(subformula.f2))))
            elif isinstance(subformula, AtomicFormula) or isinstance(formula, TrueFormula) or isinstance(formula, FalseFormula):
                return formula
            elif type(subformula) in self.derived_formulas:
                return self.to_nnf(Not(self.derived_formulas[type(subformula)](subformula)))
            else:
                raise ValueError
        else:
            raise ValueError

    @staticmethod
    def find_atomics(formula:Formula)-> Set[AtomicFormula]:
        """Finds all the atomic formulas"""
        f = formula
        res = set()
        if isinstance(f, TrueFormula) or isinstance(f, FalseFormula):
            res.add(f)
        elif isinstance(f, AtomicFormula):
            res.add(f)
        elif isinstance(f, Not):
            res = res.union(PL.find_atomics(f.f))
        elif isinstance(f, And):
            res = res.union(PL.find_atomics(f.f1)).union(PL.find_atomics(f.f2))
        elif type(f) in PL.derived_formulas:
            res = res.union(PL.find_atomics(PL.derived_formulas[type(f)](f)))
        else:
            res.add(formula)
        return res


    def models(self, f:Formula)-> Set[PLInterpretation]:
        """Find all the models of a given formula.
        Very trivial (and inefficient) algorithm: BRUTE FORCE on all the possible interpretations.
        """
        all_possible_interpretations = sorted(powerset(self.alphabet.symbols), key=len)
        models = set()
        for i in all_possible_interpretations:
            # compute current Interpretation, considering False
            # all propositional symbols not present in current interpretation
            current_interpretation = PLInterpretation(self.alphabet, {s: s in i for s in self.alphabet.symbols})
            if self.truth(f, current_interpretation):
                models.add(current_interpretation)

        return models


    def minimal_models(self, f:Formula)-> Set[PLInterpretation]:
        """Find models of min size (i.e. the less number of proposition to True)."""
        models = self.models(f)
        size2models = {}

        for m in models:
            size = len([_ for _ in m.symbol2truth if m.symbol2truth[_]])
            if size not in size2models:
                size2models[size] = set()
            size2models[size].add(m)

        if not size2models:
            return set()
        else:
            return size2models[min(size2models.keys())]
