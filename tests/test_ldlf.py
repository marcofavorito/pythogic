import unittest

from pythogic.ldlf.LDLf import LDLf
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Formula import AtomicFormula, Not, And, Or, PathExpressionUnion, PathExpressionSequence, \
    PathExpressionStar, PathExpressionTest, PathExpressionEventually
from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol


class TestLDLf(unittest.TestCase):
    """Tests for `pythogic.ltlf` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        # Symbols
        self.a_sym = Symbol("a")
        self.b_sym = Symbol("b")
        self.c_sym = Symbol("c")

        # Propositions
        self.a = AtomicFormula(self.a_sym)
        self.b = AtomicFormula(self.b_sym)
        self.c = AtomicFormula(self.c_sym)

        # Formulas
        self.not_a = Not(self.a)
        self.a_and_b = And(self.a,self.b)
        self.a_and_c = And(self.a,self.c)
        self.b_and_c = And(self.b, self.c)
        self.a_or_b = Or(self.a, self.b)

        ### Path expression
        # Propositionals
        self.prop_b_or_c =  Or(self.b, self.c)
        self.prop_a_and_b = And(self.a, self.b)
        self.prop_a_and_c = And(self.a, self.c)
        self.prop_b_and_c = And(self.b, self.c)
        # Tests
        self.test_a = PathExpressionTest(self.a)
        self.test_b = PathExpressionTest(self.b)
        # Union
        self.path_b_or_c = PathExpressionUnion(self.c, self.a)
        self.path_a_or_b = PathExpressionUnion(self.a, self.b)
        # Sequence
        self.path_a_or_b__b_or_c = PathExpressionSequence(self.path_a_or_b, self.path_b_or_c)
        # Stars
        self.path_b_or_c_star = PathExpressionStar(self.path_b_or_c)

        # Modal connective
        self.eventually_propositional_a_and_b__a_and_c = PathExpressionEventually(self.prop_a_and_b, self.a_and_c)
        self.eventually_test_a__c = PathExpressionEventually(self.test_a, self.c)
        self.eventually_test_a__b = PathExpressionEventually(self.test_a, self.b)
        self.eventually_b_or_c_star__b_and_c = PathExpressionEventually(self.path_b_or_c_star, self.b_and_c)


        self.alphabet = Alphabet({self.a_sym, self.b_sym, self.c_sym})
        # Traces
        self.ldlf = LDLf(self.alphabet)
        self.trace_1_list = [
            {self.a, self.b},
            {self.a, self.c},
            {self.a, self.b},
            {self.a, self.c},
            {self.b, self.c},
        ]
        self.trace_1 = FiniteTrace(self.trace_1_list, self.alphabet)

    def test_truth(self):
        self.assertFalse(self.ldlf.truth(self.not_a, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth (self.not_a, self.trace_1, 4))
        self.assertTrue(self.ldlf.truth (self.a_and_b, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.a_and_b, self.trace_1, 1))
        self.assertTrue(self.ldlf.truth (self.a_or_b, self.trace_1, 1))

        self.assertTrue(self.ldlf.truth (self.eventually_propositional_a_and_b__a_and_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.eventually_test_a__c, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth (self.eventually_test_a__b, self.trace_1, 0))

        # self.assertTrue(self.ldlf.truth(self.trace_1, 0, self.eventually_b_or_c_star__b_and_c))


        # self.assertTrue(self.ldlf.truth(self.trace_1, 0, self.next_a))
        # self.assertFalse(self.ldlf.truth(self.trace_1, 3, self.next_a))
        # self.assertFalse(self.ldlf.truth(self.trace_1, 4, self.next_a))
        # self.assertTrue(self.ldlf.truth(self.trace_1, 0, self.a_until_c))
        # self.assertFalse(self.ldlf.truth(self.trace_1, 4, self.b_until_a))
        # # j = 4, no k => reduces to check if c is in state j
        # self.assertTrue(self.ldlf.truth(self.trace_1, 4, self.a_until_c))
        #
        # self.assertTrue(self.ldlf.truth(self.trace_1, 0, self.true))
        # self.assertFalse(self.ldlf.truth(self.trace_1, 0, self.false))
        # self.assertTrue(self.ldlf.truth(self.trace_1, 0, self.eventually_c))
        # self.assertFalse(self.ldlf.truth(self.trace_1, 4, self.eventually_a))
        # self.assertTrue(self.ldlf.truth(self.trace_1, 4, self.always_b))
        # self.assertFalse(self.ldlf.truth(self.trace_1, 3, self.always_b))
        # self.assertFalse(self.ldlf.truth(self.trace_1, 0, self.always_a))



