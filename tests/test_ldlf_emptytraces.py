import unittest
from pprint import pprint

from pythogic.ldlf_empty_traces.LDLf_EmptyTraces import LDLf_EmptyTraces
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.base.Formula import AtomicFormula, Not, And, Or, PathExpressionUnion, PathExpressionSequence, \
    PathExpressionStar, PathExpressionTest, PathExpressionEventually, Next, Until, PathExpressionAlways, TrueFormula, \
    LogicalTrue, LogicalFalse, End, FalseFormula, LDLfLast
from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol
from pythogic.pl.PL import PL
from tests.utils import print_nfa


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
            {self.a_sym, self.b_sym},
            {self.a_sym, self.c_sym},
            {self.a_sym, self.b_sym},
            {self.a_sym, self.c_sym},
            {self.b_sym, self.c_sym},
        ]
        self.trace_1 = FiniteTrace(self.trace_1_list, self.alphabet)

    def test_truth(self):
        self.assertFalse(self.ldlf.truth(self.not_a, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.not_a, self.trace_1, 4))
        self.assertTrue(self.ldlf.truth(self.a_and_b, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.a_and_b, self.trace_1, 1))
        self.assertTrue(self.ldlf.truth(self.a_or_b, self.trace_1, 1))
        self.assertTrue(self.ldlf.truth(Not(And(self.b, self.c)), self.trace_1, 0))

        self.assertTrue(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__not_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__not_c, self.trace_1, 1))
        self.assertTrue(self.ldlf.truth(self.eventually_propositional_a_and_b__a_and_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.eventually_test_a__c, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.eventually_test_a__b, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__not_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.eventually_seq_a_and_b__a_and_c__c, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.next_a_and_c, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.liveness_b_and_c, self.trace_1, 0))
        self.assertFalse(self.ldlf.truth(self.liveness_abc, self.trace_1, 0))

        self.assertFalse(self.ldlf.truth(self.always_true__a, self.trace_1, 0))
        self.assertTrue(self.ldlf.truth(self.always_true__a, self.trace_1.segment(0, self.trace_1.length() - 1), 0))
        self.assertTrue(self.ldlf.truth(self.always_true__b_or_c, self.trace_1, 0))

        # self.assertTrue(self.ldlf.truth(self.always_not_abc__b_and_c, self.trace_1, 0))

        # self.assertTrue(self.ldlf.truth(self.trace_1, 0, self.eventually_b_or_c_star__b_and_c))


class TestLDLfEmptyTracesIsFormula(TestLDLfEmptyTraces):

    def test_is_formula_allowed_formulas(self):
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

        complex_path = PathExpressionSequence(PathExpressionUnion(and_ab, PathExpressionStar(and_ab)),
                                              PathExpressionTest(PathExpressionEventually(and_ab, tt)))
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
        # expanded_falseformula = And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        # expanded_trueformula = Not(And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC))
        expanded_falseformula = FalseFormula()
        expanded_trueformula = TrueFormula()
        expanded_end = Not(PathExpressionEventually(expanded_trueformula, Not(expanded_logicalFalse)))
        expanded_last = PathExpressionEventually(expanded_trueformula, expanded_end)
        expanded_eventually_test_tt = PathExpressionEventually(PathExpressionTest(PathExpressionEventually(self.a, tt)),
                                                               tt)

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
        self.assertEqual(self.ldlf.expand_formula(PathExpressionEventually(TrueFormula(), tt)),
                         PathExpressionEventually(expanded_trueformula, tt))
        self.assertEqual(self.ldlf.expand_formula(PathExpressionEventually(FalseFormula(), tt)),
                         PathExpressionEventually(expanded_falseformula, tt))
        self.assertEqual(self.ldlf.expand_formula(PathExpressionEventually(TrueFormula(), End())),
                         PathExpressionEventually(expanded_trueformula, expanded_end))
        self.assertEqual(self.ldlf.expand_formula(LDLfLast()), expanded_last)
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

        # to_nnf_trueformula = Or(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        # to_nnf_false_formula = And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)
        to_nnf_trueformula = TrueFormula()
        to_nnf_false_formula = FalseFormula()

        to_nnf_end = PathExpressionAlways(to_nnf_trueformula, ff)
        to_nnf_not_end = PathExpressionEventually(to_nnf_trueformula, tt)
        to_nnf_last = PathExpressionEventually(to_nnf_trueformula, to_nnf_end)
        to_nnf_not_last = PathExpressionAlways(to_nnf_trueformula, to_nnf_not_end)
        to_nnf_eventually_test_tt = PathExpressionEventually(PathExpressionTest(PathExpressionEventually(self.a, tt)),
                                                             tt)

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

        self.assertEqual(self.ldlf.to_nnf(PathExpressionEventually(TrueFormula(), tt)),
                         PathExpressionEventually(to_nnf_trueformula, tt))
        self.assertEqual(self.ldlf.to_nnf(Not(PathExpressionEventually(TrueFormula(), tt))),
                         PathExpressionAlways(to_nnf_trueformula, ff))

        self.assertEqual(self.ldlf.to_nnf(PathExpressionEventually(FalseFormula(), tt)),
                         PathExpressionEventually(to_nnf_false_formula, tt))
        self.assertEqual(self.ldlf.to_nnf(Not(PathExpressionEventually(FalseFormula(), tt))),
                         PathExpressionAlways(to_nnf_false_formula, ff))

        self.assertEqual(self.ldlf.to_nnf(PathExpressionEventually(TrueFormula(), End())),
                         PathExpressionEventually(to_nnf_trueformula, to_nnf_end))
        self.assertEqual(self.ldlf.to_nnf(Not(PathExpressionEventually(TrueFormula(), End()))),
                         PathExpressionAlways(to_nnf_trueformula, to_nnf_not_end))

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


class TestLDLfEmptyTracesDelta(TestLDLfEmptyTraces):

    def test_delta_simple_recursion(self):
        ldlf = self.ldlf
        tt = LogicalTrue()
        ff = LogicalFalse()
        and_ab = And(self.a, self.b)
        self.assertEqual(ldlf.delta(tt, frozenset()), TrueFormula())
        self.assertEqual(ldlf.delta(ff, frozenset()), FalseFormula())
        # self.assertEqual(ldlf.delta(and_ab, frozenset()), )


class TestLDLfEmptyTracesToNFA(unittest.TestCase):
    def setUp(self):
        self.a_sym = Symbol("a")
        alphabet_a = Alphabet({self.a_sym})
        self.ldlf_a = LDLf_EmptyTraces(alphabet_a)

    def test_to_nfa_alphabet_a_logical_true(self):
        """tt"""
        a = self.a_sym
        tt = LogicalTrue()
        x = self.ldlf_a.to_nfa(tt)
        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        # (frozenset([TrueFormula()]),  frozenset(),                frozenset([LogicalTrue()])),
        # (frozenset([TrueFormula()]),  frozenset({a}),             frozenset([LogicalTrue()])),
        delta = {
            (frozenset(),       frozenset(),    frozenset()),
            (frozenset([tt]),   frozenset(),    frozenset()),  # frozenset([TrueFormula()])),
            (frozenset(),       frozenset({a}), frozenset()),
            (frozenset([tt]),   frozenset({a}), frozenset())  # frozenset([TrueFormula()])),
        }

        final_states = {frozenset([LogicalTrue()]), frozenset()}
        initial_state = {frozenset([LogicalTrue()])}
        states = {frozenset([LogicalTrue()]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "00_alphabet_a_logical_true", "./tests/nfa/")

    def test_to_nfa_alphabet_a_logical_false(self):
        """ff"""
        ff = LogicalFalse()
        a = self.a_sym
        x = self.ldlf_a.to_nfa(ff)
        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(), frozenset(), frozenset()),
            (frozenset(), frozenset({a}), frozenset()),
        }

        final_states = {frozenset()}
        initial_state = {frozenset([LogicalFalse()])}
        states = {frozenset([LogicalFalse()]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "01_alphabet_a_logical_false", "./tests/nfa/")

    def test_to_nfa_alphabet_a_tt_and_tt(self):
        """tt AND tt"""
        tt = LogicalTrue()
        tt_and_tt = And(tt, tt)
        a = self.a_sym
        x = self.ldlf_a.to_nfa(tt_and_tt)

        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(),               frozenset(),    frozenset()),
            (frozenset([tt_and_tt]),    frozenset(),    frozenset()),
            (frozenset(),               frozenset({a}), frozenset()),
            (frozenset([tt_and_tt]),    frozenset({a}), frozenset())
        }
        final_states = {frozenset(),frozenset([tt_and_tt])}
        initial_state = {frozenset([tt_and_tt])}
        states = {frozenset([tt_and_tt]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "02_alphabet_a_tt_and_tt", "./tests/nfa/")


    def test_to_nfa_alphabet_a_tt_and_ff(self):
        """tt AND ff"""
        tt = LogicalTrue()
        ff = LogicalFalse()
        tt_and_ff = And(tt, ff)
        a = self.a_sym
        x = self.ldlf_a.to_nfa(tt_and_ff)

        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(), frozenset(),    frozenset()),
            (frozenset(), frozenset({a}), frozenset()),
        }
        final_states = {frozenset()}
        initial_state = {frozenset([tt_and_ff])}
        states = {frozenset([tt_and_ff]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "03_alphabet_a_tt_and_ff", "./tests/nfa/")

    def test_to_nfa_alphabet_a_tt_or_ff(self):
        """tt OR ff"""
        tt = LogicalTrue()
        ff = LogicalFalse()
        tt_or_ff = Or(tt, ff)
        a = self.a_sym
        x = self.ldlf_a.to_nfa(tt_or_ff)

        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(),              frozenset(),    frozenset()),
            (frozenset([tt_or_ff]),    frozenset(),    frozenset()),
            (frozenset(),              frozenset({a}), frozenset()),
            (frozenset([tt_or_ff]),    frozenset({a}), frozenset())
        }
        final_states = {frozenset(), frozenset([tt_or_ff])}
        initial_state = {frozenset([tt_or_ff])}
        states = {frozenset([tt_or_ff]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "04_alphabet_a_tt_and_ff", "./tests/nfa/")


    def test_to_nfa_alphabet_eventually_a_tt(self):
        """<a>tt"""
        a = self.a_sym
        tt = LogicalTrue()
        eventually_a_tt = PathExpressionEventually(AtomicFormula(a), tt)

        x = self.ldlf_a.to_nfa(eventually_a_tt)

        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(),                   frozenset(),    frozenset()),
            (frozenset([tt]),               frozenset(),    frozenset()),
            (frozenset(),                   frozenset({a}), frozenset()),
            (frozenset([eventually_a_tt]),  frozenset({a}), frozenset({tt})),
            (frozenset([tt]),               frozenset({a}), frozenset())
        }
        final_states = {frozenset(), frozenset([tt])}
        initial_state = {frozenset([eventually_a_tt])}
        states = {frozenset([eventually_a_tt]), frozenset([tt]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "05_alphabet_a_eventually_a_tt", "./tests/nfa/")

    def test_to_nfa_alphabet_eventually_a_ff(self):
        """<a>ff"""
        a = self.a_sym
        ff = LogicalFalse()
        eventually_a_ff = PathExpressionEventually(AtomicFormula(a), ff)

        x = self.ldlf_a.to_nfa(eventually_a_ff)

        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(),                   frozenset(),    frozenset()),
            (frozenset(),                   frozenset({a}), frozenset()),
            (frozenset([eventually_a_ff]),  frozenset({a}), frozenset({ff})),
        }
        final_states = {frozenset()}
        initial_state = {frozenset([eventually_a_ff])}
        states = {frozenset([eventually_a_ff]), frozenset([ff]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "06_alphabet_a_eventually_a_ff", "./tests/nfa/")

    def test_to_nfa_alphabet_a_propositional_a(self):
        """a === <a>tt"""
        a = self.a_sym
        tt = LogicalTrue()
        atomic_a = AtomicFormula(a)
        eventually_a_tt = PathExpressionEventually(atomic_a, tt)

        self.assertEqual(self.ldlf_a.to_nfa(atomic_a), self.ldlf_a.to_nfa(eventually_a_tt))

    def test_to_nfa_alphabet_a_propositional_false(self):
        """false"""
        a = self.a_sym
        tt = LogicalTrue()
        eventually_false_tt = PathExpressionEventually(FalseFormula(), tt)
        aaa = self.ldlf_a.expand_formula(eventually_false_tt)

        pl = PL(self.ldlf_a.alphabet)
        expanded_false = pl.expand_formula(FalseFormula())
        expanded_eventually_false_tt = PathExpressionEventually(expanded_false, tt)
        x = self.ldlf_a.to_nfa(eventually_false_tt)

        pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(), frozenset(),    frozenset()),
            (frozenset(), frozenset({a}), frozenset()),
        }
        final_states = {frozenset()}
        initial_state = {frozenset([expanded_eventually_false_tt])}
        states = {frozenset([expanded_eventually_false_tt]), frozenset()}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "07_alphabet_a_eventually_false_tt", "./tests/nfa/")


    def test_to_nfa_alphabet_a_propositional_true(self):
        """false"""
        a = self.a_sym
        tt = LogicalTrue()
        eventually_true_tt = PathExpressionEventually(TrueFormula(), tt)

        x = self.ldlf_a.to_nfa(eventually_true_tt)

        # pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(),                       frozenset(),    frozenset()),
            (frozenset(),                       frozenset({a}), frozenset()),
            (frozenset({eventually_true_tt}), frozenset(), frozenset({tt})),
            (frozenset({eventually_true_tt}), frozenset({a}), frozenset({tt})),
            (frozenset({tt}),                   frozenset(),    frozenset()),
            (frozenset({tt}),                   frozenset({a}), frozenset()),

        }
        final_states = {frozenset(), frozenset([tt])}
        initial_state = {frozenset([eventually_true_tt])}
        states = {frozenset(), frozenset([eventually_true_tt]), frozenset([tt])}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "08_alphabet_a_eventually_true_tt", "./tests/nfa/")


    def test_to_nfa_alphabet_a_propositional_true(self):
        """false"""
        a = self.a_sym
        tt = LogicalTrue()
        eventually_true_tt = PathExpressionEventually(TrueFormula(), tt)

        x = self.ldlf_a.to_nfa(eventually_true_tt)

        pprint(x)
        alphabet = {frozenset(), frozenset({a})}

        delta = {
            (frozenset(),                       frozenset(),    frozenset()),
            (frozenset(),                       frozenset({a}), frozenset()),
            (frozenset({eventually_true_tt}),   frozenset(), frozenset({tt})),
            (frozenset({eventually_true_tt}),   frozenset({a}), frozenset({tt})),
            (frozenset({tt}),                   frozenset(),    frozenset()),
            (frozenset({tt}),                   frozenset({a}), frozenset()),

        }
        final_states = {frozenset(), frozenset([tt])}
        initial_state = {frozenset([eventually_true_tt])}
        states = {frozenset(), frozenset([eventually_true_tt]), frozenset([tt])}

        self.assertEqual(x["alphabet"], alphabet)
        self.assertEqual(x["states"], states)
        self.assertEqual(x["initial_states"], initial_state)
        self.assertEqual(x["accepting_states"], final_states)
        self.assertEqual(x["transitions"], delta)

        print_nfa(x, "08_alphabet_a_eventually_true_tt", "./tests/nfa/")

