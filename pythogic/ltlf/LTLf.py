
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Formula import AtomicFormula, Next, Until, Formula, TrueFormula, FalseFormula, UnaryOperator, \
    BinaryOperator, Not, And, LDLfLast, Or, Eventually, Always, DUMMY_ATOMIC
from pythogic.base.Alphabet import Alphabet
from pythogic.base.FormalSystem import FormalSystem
from pythogic.base.Symbol import DUMMY_SYMBOL


class LTLf(FormalSystem):
    def __init__(self, alphabet: Alphabet):
        super().__init__(alphabet)

    allowed_formulas = {AtomicFormula, Not, And, Next, Until}
    derived_formulas = {TrueFormula, FalseFormula, LDLfLast, Or, Eventually, Always}

    def _is_formula(self, f: Formula):
        """Check if a formula is legal in the current formal system"""
        if isinstance(f, AtomicFormula):
            return f.symbol in self.alphabet.symbols or f == AtomicFormula(DUMMY_SYMBOL)
        elif isinstance(f, UnaryOperator):
            return self.is_formula(f.f)
        elif isinstance(f, BinaryOperator):
            return self.is_formula(f.f1) and self.is_formula(f.f2)
        elif isinstance(f, TrueFormula) or isinstance(f, FalseFormula):
            return True
        else:
            raise ValueError("Argument not a valid Formula")

    def _truth(self, formula: Formula, trace: FiniteTrace, position: int):
        assert self._is_formula(formula)
        assert trace.alphabet == self.alphabet
        truth = self.truth
        if isinstance(formula, AtomicFormula):
            return formula in trace.get(position)
        elif isinstance(formula, Not):
            return not truth(formula.f, trace, position)
        elif isinstance(formula, And):
            return truth(formula.f1, trace, position) and truth(formula.f2, trace, position)
        elif isinstance(formula, Next):
            return position < trace.last() and truth(formula.f, trace, position+1)
        elif isinstance(formula, Until):
            return any(
                truth(formula.f2, trace, j)
                and all(
                    truth(formula.f1, trace, k) for k in range(position, j)
                )
                for j in range(position, trace.last() + 1)
            )
        else:
            raise ValueError("Not valid formula")


    def to_equivalent_formula(self, derived_formula:Formula):
        if isinstance(derived_formula, Or):
            return Not(And(Not(derived_formula.f1), Not(derived_formula.f2)))
        elif isinstance(derived_formula, Always):
            return Not(Eventually(Not(derived_formula.f)))
        elif isinstance(derived_formula, Eventually):
            return Until(TrueFormula(), derived_formula.f)
        elif isinstance(derived_formula, FalseFormula):
            return And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        elif isinstance(derived_formula, TrueFormula):
            return Not(FalseFormula())
        elif isinstance(derived_formula, LDLfLast):
            return Next(TrueFormula(), FalseFormula())
        else:
            raise ValueError("Derived formula not recognized")


    def _expand_formula(self, f:Formula):
        if isinstance(f, AtomicFormula):
            return f
        elif isinstance(f, And):
            return And(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Not):
            return Not(self.expand_formula(f.f))
        elif isinstance(f, Until):
            return Until(self.expand_formula(f.f1), self.expand_formula(f.f2))
        elif isinstance(f, Next):
            return Next(self.expand_formula(f.f))
        else:
            raise ValueError("Not valid Formula to expand")


    def to_nnf(self, f:Formula):
        pass
