import unittest

from pythogic.ldlf.LDLf import LDLf
from pythogic.ldlf_empty_traces.LDLf_EmptyTraces import LDLf_EmptyTraces
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Formula import AtomicFormula, Not, And, Or, PathExpressionUnion, PathExpressionSequence, \
    PathExpressionStar, PathExpressionTest, PathExpressionEventually, Next, Until, PathExpressionAlways, TrueFormula, \
    LogicalTrue, LogicalFalse, End, FalseFormula, LDLfLast, DUMMY_ATOMIC
from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol

class TestLDLfEmptyTraces(unittest.TestCase):
    """Tests for `pythogic.ldlf_empty_traces` package."""
    def setUp(self):
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
        self.a_and_b = And(self.a, self.b)
        self.a_and_c = And(self.a, self.c)
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
        self.eventually_seq_a_and_b__a_and_c__not_c = PathExpressionEventually(self.path_seq_a_and_b__a_and_c,
                                                                               self.not_c)
        self.eventually_seq_a_and_b__a_and_c__c = PathExpressionEventually(self.path_seq_a_and_b__a_and_c, self.c)
        self.eventually_b_or_c_star__b_and_c = PathExpressionEventually(self.path_b_or_c_star, self.b_and_c)

        self.next_a_and_c = PathExpressionEventually(TrueFormula(), self.a_and_c)
        self.liveness_b_and_c = PathExpressionEventually(PathExpressionStar(TrueFormula()), self.b_and_c)
        self.liveness_abc = PathExpressionEventually(PathExpressionStar(TrueFormula()), self.abc)

        self.always_true__a = PathExpressionAlways(PathExpressionStar(TrueFormula()), self.a)
        self.always_true__b_or_c = PathExpressionAlways(PathExpressionStar(TrueFormula()), self.b_or_c)

        self.alphabet = Alphabet({self.a_sym, self.b_sym, self.c_sym})
        # Traces
        self.ldlf = LDLf_EmptyTraces(self.alphabet)
        self.trace_1_list = [
            {self.a, self.b},
            {self.a, self.c},
            {self.a, self.b},
            {self.a, self.c},
            {self.b, self.c},
        ]
        self.trace_1 = FiniteTrace(self.trace_1_list, self.alphabet)

class TestLDLfEmptyTracesIsFormula(TestLDLfEmptyTraces):

    def test_is_formula_allowed_formulas(self):
        tt = LogicalTrue()
        and_tt = And(tt,tt)
        and_ab = And(self.a, self.b)
        test_tt = PathExpressionTest(tt)

        eventually_atomic_tt = PathExpressionEventually(self.a,tt)
        eventually_not_tt = PathExpressionEventually(Not(self.a), tt)
        eventually_and_tt = PathExpressionEventually(and_ab, tt)
        eventually_and_tt_error = PathExpressionEventually(And(self.a, AtomicFormula.fromName("d")), tt)
        eventually_test_tt = PathExpressionEventually(test_tt, tt)
        eventually_union_tt = PathExpressionEventually(PathExpressionUnion(test_tt, and_ab), tt)
        eventually_sequence_tt = PathExpressionEventually(PathExpressionSequence(test_tt, and_ab), tt)
        eventually_star_tt = PathExpressionEventually(PathExpressionSequence(test_tt, and_ab), tt)

        self.assertTrue(self.ldlf.is_formula(tt))
        self.assertTrue(self.ldlf.is_formula(Not(tt)))
        self.assertTrue(self.ldlf.is_formula(and_tt))
        self.assertTrue(self.ldlf.is_formula(eventually_atomic_tt))
        self.assertTrue(self.ldlf.is_formula(eventually_not_tt))
        self.assertTrue(self.ldlf.is_formula(eventually_and_tt))
        # introduce a new symbol
        self.assertFalse(self.ldlf.is_formula(eventually_and_tt_error))
        self.assertTrue(self.ldlf.is_formula(eventually_test_tt))
        self.assertTrue(self.ldlf.is_formula(eventually_sequence_tt))
        self.assertTrue(self.ldlf.is_formula(eventually_union_tt))
        self.assertTrue(self.ldlf.is_formula(eventually_star_tt))

    def test_is_formula_allowed_formulas_combinations(self):
        tt = LogicalTrue()
        and_tt = And(tt, Not(tt))
        and_ab = And(self.a, self.b)

        complex_path = PathExpressionSequence(PathExpressionUnion(and_ab, PathExpressionStar(and_ab)), PathExpressionTest(PathExpressionEventually(and_ab,tt)))
        complex_eventually = PathExpressionEventually(complex_path, and_tt)

        self.assertTrue(self.ldlf.is_formula(complex_eventually))

    def test_is_formula_derived_formulas(self):
        tt = LogicalTrue()
        and_tt = And(tt, tt)
        and_ab = And(self.a, self.b)
        eventually_test_tt = PathExpressionEventually(PathExpressionTest(self.a), tt)
        eventually_test_tt_error = PathExpressionEventually(PathExpressionTest(AtomicFormula.fromName("d")), tt)


        self.assertTrue(self.ldlf.is_formula(LogicalFalse()))
        self.assertTrue(self.ldlf.is_formula(Or(tt, tt)))
        self.assertTrue(self.ldlf.is_formula(Next(tt)))
        self.assertTrue(self.ldlf.is_formula(Until(Next(tt), tt)))
        self.assertTrue(self.ldlf.is_formula(Until(Next(tt), tt)))
        self.assertTrue(self.ldlf.is_formula(End()))
        self.assertTrue(self.ldlf.is_formula(PathExpressionAlways(and_ab, and_tt)))
        self.assertTrue(self.ldlf.is_formula(PathExpressionAlways(TrueFormula(), and_tt)))
        self.assertTrue(self.ldlf.is_formula(PathExpressionAlways(FalseFormula(), and_tt)))
        self.assertTrue(self.ldlf.is_formula(LDLfLast()))
        # a propositional is not an elementary formula
        self.assertTrue(self.ldlf.is_formula(and_ab))
        self.assertFalse(self.ldlf.is_formula(And(self.a, AtomicFormula.fromName("d"))))
        # a propositional is not an elementary formula, neither in the Test expression
        self.assertTrue(self.ldlf.is_formula(eventually_test_tt))
        self.assertFalse(self.ldlf.is_formula(eventually_test_tt_error))


class TestLDLfEmptyTracesExpandFormula(TestLDLfEmptyTraces):
    def test_expand_formula_allowed_formula(self):
        """Expansion of elementary formula should return the same formula."""
        tt = LogicalTrue()
        and_tt = And(tt, tt)
        and_ab = And(self.a, self.b)
        test_tt = PathExpressionTest(tt)

        eventually_atomic_tt = PathExpressionEventually(self.a, tt)
        eventually_not_tt = PathExpressionEventually(Not(self.a), tt)
        eventually_and_tt = PathExpressionEventually(and_ab, tt)
        eventually_and_tt_error = PathExpressionEventually(And(self.a, AtomicFormula.fromName("d")), tt)
        eventually_test_tt = PathExpressionEventually(test_tt, tt)
        eventually_union_tt = PathExpressionEventually(PathExpressionUnion(test_tt, and_ab), tt)
        eventually_sequence_tt = PathExpressionEventually(PathExpressionSequence(test_tt, and_ab), tt)
        eventually_star_tt = PathExpressionEventually(PathExpressionSequence(test_tt, and_ab), tt)

        self.assertEqual(self.ldlf.expand_formula(tt), tt)
        self.assertEqual(self.ldlf.expand_formula(Not(tt)), Not(tt))
        self.assertEqual(self.ldlf.expand_formula(and_tt), and_tt)
        self.assertEqual(self.ldlf.expand_formula(eventually_atomic_tt), eventually_atomic_tt)
        self.assertEqual(self.ldlf.expand_formula(eventually_not_tt), eventually_not_tt)
        self.assertEqual(self.ldlf.expand_formula(eventually_and_tt), eventually_and_tt)
        # introduce a new symbol. Notice: it does not throw error
        self.assertEqual(self.ldlf.expand_formula(eventually_and_tt_error), eventually_and_tt_error)
        self.assertEqual(self.ldlf.expand_formula(eventually_test_tt), eventually_test_tt)
        self.assertEqual(self.ldlf.expand_formula(eventually_sequence_tt), eventually_sequence_tt)
        self.assertEqual(self.ldlf.expand_formula(eventually_union_tt), eventually_union_tt)
        self.assertEqual(self.ldlf.expand_formula(eventually_star_tt), eventually_star_tt)


    def test_expand_formula_derived_formula(self):
        tt = LogicalTrue()
        and_ab = And(self.a, self.b)
        eventually_test_tt = PathExpressionEventually(PathExpressionTest(self.a), tt)

        expanded_logicalFalse = Not(tt)
        expanded_falseformula = And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        expanded_trueformula = Not(And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC))
        expanded_end = Not(PathExpressionEventually(expanded_trueformula, Not(expanded_logicalFalse)))
        expanded_last = PathExpressionEventually(expanded_trueformula, expanded_end)
        expanded_eventually_test_tt = PathExpressionEventually(PathExpressionTest(PathExpressionEventually(self.a, tt)), tt)

        always_ = PathExpressionAlways(and_ab, tt)
        next_ = Next(tt)
        until_ = Until(tt, tt)
        expanded_always_ = Not(PathExpressionEventually(and_ab, Not(tt)))
        expanded_next_ = PathExpressionEventually(expanded_trueformula, And(tt, Not(expanded_end)))
        expanded_until = PathExpressionEventually(
                PathExpressionStar(PathExpressionSequence(PathExpressionTest(tt), expanded_trueformula)),
                And(tt, Not(expanded_end))
        )


        self.assertEqual(self.ldlf.expand_formula(LogicalFalse()), expanded_logicalFalse)
        self.assertEqual(self.ldlf.expand_formula(Or(tt, tt)), Not(And(Not(tt), Not(tt))))
        self.assertEqual(self.ldlf.expand_formula(always_), expanded_always_)
        self.assertEqual(self.ldlf.expand_formula(PathExpressionEventually(TrueFormula(), tt)), PathExpressionEventually(expanded_trueformula, tt))
        self.assertEqual(self.ldlf.expand_formula(PathExpressionEventually(FalseFormula(), tt)), PathExpressionEventually(expanded_falseformula, tt))
        self.assertEqual(self.ldlf.expand_formula(PathExpressionEventually(TrueFormula(), End())),PathExpressionEventually(expanded_trueformula, expanded_end))
        self.assertEqual(self.ldlf.expand_formula(LDLfLast()),expanded_last)
        self.assertEqual(self.ldlf.expand_formula(next_), expanded_next_)
        self.assertEqual(self.ldlf.expand_formula(until_), expanded_until)
        # a propositional is not an elementary formula
        self.assertEqual(self.ldlf.expand_formula(and_ab), PathExpressionEventually(and_ab, tt))
        # a propositional is not an elementary formula, neither in the Test expression
        self.assertEqual(self.ldlf.expand_formula(eventually_test_tt), expanded_eventually_test_tt)

class TestLDLfEmptyTracesToNNF(TestLDLfEmptyTraces):

    def test_to_nnf_allowed_formulas(self):
        tt = LogicalTrue()
        ff = LogicalFalse()
        and_tt = And(tt, tt)
        and_ab = And(self.a, self.b)
        test_tt = PathExpressionTest(tt)

        eventually_atomic_tt = PathExpressionEventually(self.a, tt)
        eventually_not_tt = PathExpressionEventually(Not(self.a), tt)
        eventually_and_tt = PathExpressionEventually(and_ab, tt)
        eventually_and_tt_error = PathExpressionEventually(And(self.a, AtomicFormula.fromName("d")), tt)
        eventually_test_tt = PathExpressionEventually(test_tt, tt)
        eventually_union_tt = PathExpressionEventually(PathExpressionUnion(test_tt, and_ab), tt)
        eventually_sequence_tt = PathExpressionEventually(PathExpressionSequence(test_tt, and_ab), tt)
        eventually_star_tt = PathExpressionEventually(PathExpressionSequence(test_tt, and_ab), tt)

        self.assertEqual(self.ldlf.to_nnf(tt), tt)
        self.assertEqual(self.ldlf.to_nnf(Not(tt)), ff)
        self.assertEqual(self.ldlf.to_nnf(Not(and_tt)), Or(ff, ff))
        self.assertEqual(self.ldlf.to_nnf(eventually_atomic_tt), eventually_atomic_tt)
        self.assertEqual(self.ldlf.to_nnf(eventually_not_tt), eventually_not_tt)
        self.assertEqual(self.ldlf.to_nnf(eventually_and_tt), eventually_and_tt)
        self.assertEqual(self.ldlf.to_nnf(eventually_test_tt), eventually_test_tt)
        self.assertEqual(self.ldlf.to_nnf(eventually_sequence_tt), eventually_sequence_tt)
        self.assertEqual(self.ldlf.to_nnf(eventually_union_tt), eventually_union_tt)
        self.assertEqual(self.ldlf.to_nnf(eventually_star_tt), eventually_star_tt)

        with self.assertRaises(AssertionError):
            # introduce a new symbol. Throws an error
            self.ldlf.to_nnf(eventually_and_tt_error)

    def test_to_nnf_derived_formulas(self):
        tt = LogicalTrue()
        ff = LogicalFalse()
        and_ab = And(self.a, self.b)
        eventually_test_tt = PathExpressionEventually(PathExpressionTest(self.a), tt)

        to_nnf_trueformula = Or(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        to_nnf_false_formula = And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        to_nnf_end = PathExpressionAlways(to_nnf_trueformula, ff)
        to_nnf_not_end = PathExpressionEventually(to_nnf_trueformula, tt)
        to_nnf_last = PathExpressionEventually(to_nnf_trueformula, to_nnf_end)
        to_nnf_not_last = PathExpressionAlways(to_nnf_trueformula, to_nnf_not_end)
        to_nnf_eventually_test_tt = PathExpressionEventually(PathExpressionTest(PathExpressionEventually(self.a, tt)),tt)

        always_ = PathExpressionAlways(and_ab, tt)
        not_always_ = PathExpressionEventually(and_ab, ff)

        next_ = Next(tt)
        until_ = Until(tt, tt)
        to_nnf_next_ = PathExpressionEventually(to_nnf_trueformula, And(tt, to_nnf_not_end))
        to_nnf_not_next_ = PathExpressionAlways(to_nnf_trueformula, Or(ff, to_nnf_end))
        to_nnf_until_ = PathExpressionEventually(
            PathExpressionStar(PathExpressionSequence(PathExpressionTest(tt), to_nnf_trueformula)),
            And(tt, to_nnf_not_end)
        )
        to_nnf_not_until_ = PathExpressionAlways(
            PathExpressionStar(PathExpressionSequence(PathExpressionTest(tt), to_nnf_trueformula)),
            Or(ff, to_nnf_end)
        )

        self.assertEqual(self.ldlf.to_nnf(ff), ff)
        self.assertEqual(self.ldlf.to_nnf(Or(tt, tt)), Or(tt, tt))

        self.assertEqual(self.ldlf.to_nnf(always_), always_)
        self.assertEqual(self.ldlf.to_nnf(Not(always_)), not_always_)

        self.assertEqual(self.ldlf.to_nnf(PathExpressionEventually(TrueFormula(), tt)),  PathExpressionEventually(to_nnf_trueformula, tt))
        self.assertEqual(self.ldlf.to_nnf(Not(PathExpressionEventually(TrueFormula(), tt))), PathExpressionAlways(to_nnf_trueformula, ff))

        self.assertEqual(self.ldlf.to_nnf(PathExpressionEventually(FalseFormula(), tt)), PathExpressionEventually(to_nnf_false_formula, tt))
        self.assertEqual(self.ldlf.to_nnf(Not(PathExpressionEventually(FalseFormula(), tt))),PathExpressionAlways(to_nnf_false_formula, ff))

        self.assertEqual(self.ldlf.to_nnf(PathExpressionEventually(TrueFormula(), End())), PathExpressionEventually(to_nnf_trueformula, to_nnf_end))
        self.assertEqual(self.ldlf.to_nnf(Not(PathExpressionEventually(TrueFormula(), End()))), PathExpressionAlways(to_nnf_trueformula, to_nnf_not_end))

        self.assertEqual(self.ldlf.to_nnf(LDLfLast()), to_nnf_last)
        self.assertEqual(self.ldlf.to_nnf(Not(LDLfLast())), to_nnf_not_last)

        self.assertEqual(self.ldlf.to_nnf(next_), to_nnf_next_)
        self.assertEqual(self.ldlf.to_nnf(Not(next_)), to_nnf_not_next_)

        self.assertEqual(self.ldlf.to_nnf(until_), to_nnf_until_)
        self.assertEqual(self.ldlf.to_nnf(Not(until_)), to_nnf_not_until_)

        # a propositional is not an elementary formula
        self.assertEqual(self.ldlf.to_nnf(and_ab), PathExpressionEventually(and_ab, tt))
        # a propositional is not an elementary formula, neither in the Test expression
        self.assertEqual(self.ldlf.to_nnf(eventually_test_tt), to_nnf_eventually_test_tt)






