import unittest

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol
from pythogic.pl.PL import PL
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.base.Formula import AtomicFormula, TrueFormula, FalseFormula, Not, And, Or, Implies, Next, Equivalence, \
    DUMMY_ATOMIC


class TestPL(unittest.TestCase):
    """Tests for `pythogic.ltlf` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.a_sym = Symbol("a")
        self.b_sym = Symbol("b")
        self.c_sym = Symbol("c")
        self.alphabet = Alphabet({self.a_sym, self.b_sym, self.c_sym})

        # Propositions
        self.a = AtomicFormula(self.a_sym)
        self.b = AtomicFormula(self.b_sym)
        self.c = AtomicFormula(self.c_sym)

        self.not_a = Not(self.a)
        self.not_a_and_b = And(self.not_a, self.b)
        self.not_a_or_c = Or(self.not_a, self.c)
        self.true = TrueFormula()
        self.false = FalseFormula()


        self.symbol2truth = {
            self.a_sym: True,
            self.b_sym: False,
            self.c_sym: True
        }
        self.I = PLInterpretation(self.alphabet, self.symbol2truth)
        self.PL = PL(self.alphabet)


    def tearDown(self):
        """Tear down test fixtures, if any."""


    def test_truth(self):
        self.assertTrue(self.PL.truth (self.a, self.I))
        self.assertFalse(self.PL.truth(self.b, self.I))
        self.assertTrue(self.PL.truth (self.c, self.I))

        self.assertFalse(self.PL.truth(self.not_a, self.I))
        self.assertFalse(self.PL.truth(self.not_a_and_b, self.I))
        self.assertTrue(self. PL.truth (self.not_a_or_c, self.I))

        self.assertTrue(self. PL.truth (self.true, self.I))
        self.assertFalse(self.PL.truth(self.false, self.I))


class TestPLIsFormula(unittest.TestCase):

    def test_is_formula_atomic(self):
        a_sym = Symbol("a")
        alphabet = Alphabet({a_sym})
        a = AtomicFormula(a_sym)
        pl = PL(alphabet)
        self.assertTrue(pl.is_formula(a))

    def test_is_formula_composed(self):
        a_sym = Symbol("a")
        alphabet = Alphabet({a_sym})
        a = AtomicFormula(a_sym)
        pl = PL(alphabet)
        self.assertTrue(pl.is_formula(Implies(Not(a), And(TrueFormula(), Not(FalseFormula())))))
        self.assertFalse(pl.is_formula(Implies(Not(a), And(TrueFormula(), Next(FalseFormula())))))

    def test_is_formula_error(self):
        a_sym = Symbol("a")
        alphabet = Alphabet({a_sym})
        a = Next(AtomicFormula(a_sym))
        pl = PL(alphabet)
        self.assertFalse(pl.is_formula(a))


class TestPLExpandFormula(unittest.TestCase):
    def test_expand_formula_allowed_formulas(self):
        a_sym = Symbol("a")
        b_sym = Symbol("b")
        alphabet = Alphabet({a_sym, b_sym})
        a = AtomicFormula(a_sym)
        b = AtomicFormula(b_sym)
        pl = PL(alphabet)
        self.assertEqual(pl.expand_formula(a), a)
        self.assertEqual(pl.expand_formula(Not(b)), Not(b))
        self.assertEqual(pl.expand_formula(And(a,b)), And(a,b))

    def test_expand_formula_derived_formulas(self):
        a_sym = Symbol("a")
        b_sym = Symbol("b")
        alphabet = Alphabet({a_sym, b_sym})
        a = AtomicFormula(a_sym)
        b = AtomicFormula(b_sym)
        T = Not(And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC))
        F = And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        pl = PL(alphabet)
        self.assertEqual(pl.expand_formula(TrueFormula()), T)
        self.assertEqual(pl.expand_formula(FalseFormula()), F)
        self.assertEqual(pl.expand_formula(Or(a, b)), Not(And(Not(a), Not(b))))
        self.assertEqual(pl.expand_formula(Implies(a, b)), Not(And(a, Not(b))))
        # A === B = (A AND B) OR (NOT A AND NOT B) = NOT( NOT(A AND B) AND NOT(NOT A AND NOT B) )
        self.assertEqual(pl.expand_formula(Equivalence(a, b)), Not(And(Not(And(a, b)), Not(And(Not(a), Not(b))))))


    def test_expand_formula_composed(self):
        a_sym = Symbol("a")
        alphabet = Alphabet({a_sym})
        a = AtomicFormula(a_sym)
        T = Not(And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC))
        F = And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        pl = PL(alphabet)
        self.assertEqual(pl.expand_formula(And(TrueFormula(), FalseFormula())), And(T, F))
        self.assertEqual(pl.expand_formula(Or(TrueFormula(), FalseFormula())), Not(And(Not(T), Not(F))))
        self.assertEqual(pl.expand_formula(Implies(TrueFormula(), FalseFormula())), Not(And(T, Not(F))))
        self.assertEqual(pl.expand_formula(Equivalence(TrueFormula(), FalseFormula())), Not(And(Not(And(T, F)), Not(And(Not(T), Not(F))))))

    def test_expand_formula_error(self):
        a_sym = Symbol("a")
        alphabet = Alphabet({a_sym})
        a = Next(AtomicFormula(a_sym))
        pl = PL(alphabet)

        with self.assertRaises(ValueError) as ve:
            pl.expand_formula(a)


class TestPLToNNF(unittest.TestCase):
    def test_to_nnf_allowed_formulas(self):
        a_sym = Symbol("a")
        b_sym = Symbol("b")
        alphabet = Alphabet({a_sym, b_sym})
        a = AtomicFormula(a_sym)
        b = AtomicFormula(b_sym)
        pl = PL(alphabet)
        self.assertEqual(pl.to_nnf(a), a)
        self.assertEqual(pl.to_nnf(Not(b)), Not(b))
        self.assertEqual(pl.to_nnf(And(a,b)), And(a,b))

    def test_to_nnf_allowed_formulas_not_normalized(self):
        a_sym = Symbol("a")
        b_sym = Symbol("b")
        alphabet = Alphabet({a_sym, b_sym})
        a = AtomicFormula(a_sym)
        b = AtomicFormula(b_sym)
        pl = PL(alphabet)
        self.assertEqual(pl.to_nnf(Not(Not(b))), b)
        self.assertEqual(pl.to_nnf(Not(And(a, Not(b)))), Or(Not(a), b))

    def test_to_nnf_derived_formula(self):
        a_sym = Symbol("a")
        b_sym = Symbol("b")
        alphabet = Alphabet({a_sym, b_sym})
        a = AtomicFormula(a_sym)
        b = AtomicFormula(b_sym)
        pl = PL(alphabet)
        self.assertEqual(pl.to_nnf(Not(Or(b, Not(a)))), And(Not(b), a))
        self.assertEqual(pl.to_nnf(Not(Implies(b, Not(a)))), And(b, a))
