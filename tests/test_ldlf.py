import unittest

from pythogic.ldlf.LDLf import LDLf
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Formula import AtomicFormula, Not, And, Or, PathExpressionUnion, PathExpressionSequence, \
    PathExpressionStar, PathExpressionTest, PathExpressionEventually, Next, Until, PathExpressionAlways, TrueFormula
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

        # Propositionals
        self.not_a = Not(self.a)
        self.not_b = Not(self.b)
        self.not_c = Not(self.c)
        self.a_and_b = And(self.a,self.b)
        self.a_and_c = And(self.a,self.c)
        self.b_and_c = And(self.b, self.c)
        self.abc = And(self.a, And(self.b, self.c))
        self.b_or_c = Or(self.b, self.c)
        self.a_or_b = Or(self.a, self.b)
        self.not_abc = Not(And(self.a, And(self.b, self.c)))

        ### Path expression
        # Tests
        self.test_a = PathExpressionTest(self.a)
        self.test_b = PathExpressionTest(self.b)
        self.test_not_a = PathExpressionTest(self.not_a)
        self.test_not_b = PathExpressionTest(self.not_b)
        # Union
        self.path_a_or_b = PathExpressionUnion(self.a, self.b)
        self.path_b_or_c = PathExpressionUnion(self.b, self.c)
        # Sequence
        self.path_seq_a_and_b__a_and_c = PathExpressionSequence(self.a_and_b, self.a_and_c)
        self.path_a_or_b__b_or_c = PathExpressionSequence(self.path_a_or_b, self.path_b_or_c)
        # Stars
        self.path_b_or_c_star = PathExpressionStar(self.path_b_or_c)
        self.path_not_abc = PathExpressionStar(self.not_abc)

        # Modal connective
        self.eventually_propositional_a_and_b__a_and_c = PathExpressionEventually(self.a_and_b, self.a_and_c)
        self.eventually_test_a__c = PathExpressionEventually(self.test_a, self.c)
        self.eventually_test_a__b = PathExpressionEventually(self.test_a, self.b)
        self.eventually_seq_a_and_b__a_and_c__not_c = PathExpressionEventually(self.path_seq_a_and_b__a_and_c, self.not_c)
        self.eventually_seq_a_and_b__a_and_c__c = PathExpressionEventually(self.path_seq_a_and_b__a_and_c, self.c)
        self.eventually_b_or_c_star__b_and_c = PathExpressionEventually(self.path_b_or_c_star, self.b_and_c)

        self.next_a_and_c = PathExpressionEventually(TrueFormula(), self.a_and_c)
        self.liveness_b_and_c = PathExpressionEventually(PathExpressionStar(TrueFormula()), self.b_and_c)
        self.liveness_abc= PathExpressionEventually(PathExpressionStar(TrueFormula()), self.abc)

        self.always_true__a = PathExpressionAlways(PathExpressionStar(TrueFormula()), self.a)
        self.always_true__b_or_c =    PathExpressionAlways(PathExpressionStar(TrueFormula()), self.b_or_c)

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
        self.assertTrue(self.ldlf.truth(Not(And(self.b, self.c)), self.trace_1, 0))

        self.assertTrue(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__not_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__not_c, self.trace_1, 1))
        self.assertTrue(self.ldlf.truth (self.eventually_propositional_a_and_b__a_and_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.eventually_test_a__c, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth (self.eventually_test_a__b, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__not_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__c, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.next_a_and_c, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.liveness_b_and_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.liveness_abc, self.trace_1, 0))

        self.assertFalse(self.ldlf.truth(self.always_true__a, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.always_true__a, self.trace_1.segment(0,self.trace_1.length()-1), 0))
        self.assertTrue(self.ldlf.truth(self.always_true__b_or_c, self.trace_1, 0))

        # self.assertTrue(self.ldlf.truth(self.always_not_abc__b_and_c, self.trace_1, 0))

        # self.assertTrue(self.ldlf.truth(self.trace_1, 0, self.eventually_b_or_c_star__b_and_c))


    def test_to_nnf(self):
        f1 = Not(PathExpressionEventually(PathExpressionSequence(
            PathExpressionTest(Not(self.a_and_b)),
            PathExpressionStar(TrueFormula())), self.abc)
        )
        nnf_f1 = PathExpressionAlways(PathExpressionSequence(
            PathExpressionTest(Or(Not(self.a), Not(self.b))),
            PathExpressionStar(TrueFormula())
        ), Or(Not(self.a), Or(Not(self.b), Not(self.c))))

        self.assertEqual(self.ldlf.to_nnf(f1), nnf_f1)






