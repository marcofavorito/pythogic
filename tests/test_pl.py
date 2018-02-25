import unittest

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol
from pythogic.pl.PL import PL
from pythogic.pl.semantics.PLInterpretation import PLInterpretation
from pythogic.base.Formula import AtomicFormula, TrueFormula, FalseFormula, Not, And, Or


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
        self.assertTrue(self.PL.truth (self.not_a_or_c, self.I))

        self.assertTrue(self.PL.truth (self.true, self.I))
        self.assertFalse(self.PL.truth(self.false, self.I))





