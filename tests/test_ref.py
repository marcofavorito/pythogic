#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythogic` package."""

import unittest

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Formula import AtomicFormula, PathExpressionSequence, PathExpressionUnion, PathExpressionStar, And, \
    Not, Or, TrueFormula, FalseFormula
from pythogic.base.Symbol import Symbol
from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.ref.REf import REf


class TestREf(unittest.TestCase):
    """Tests for `pythogic.ref` package."""

    def setUp(self):
        pass


    def tearDown(self):
        pass


class TestREfIsFormula(unittest.TestCase):
    def test_propositional_is_formula(self):
        alphabet = Alphabet.fromStrings({"a"})
        a = AtomicFormula.fromName("a")
        ref = REf(alphabet)
        self.assertTrue(ref.is_formula(a))

    def test_union(self):
        alphabet = Alphabet.fromStrings({"a", "b"})
        a = AtomicFormula.fromName("a")
        b = AtomicFormula.fromName("b")
        ref = REf(alphabet)
        self.assertTrue(ref.is_formula(PathExpressionUnion(a,b)))

    def test_sequence(self):
        alphabet = Alphabet.fromStrings({"a", "b"})
        a = AtomicFormula.fromName("a")
        b = AtomicFormula.fromName("b")
        ref = REf(alphabet)
        self.assertTrue(ref.is_formula(PathExpressionSequence(a, b)))


    def test_star(self):
        alphabet = Alphabet.fromStrings({"a"})
        a = AtomicFormula.fromName("a")
        ref = REf(alphabet)
        self.assertTrue(ref.is_formula(PathExpressionStar(a)))


class TestREfTruth(unittest.TestCase):

    def setUp(self):
        # Symbols
        self.a_sym = Symbol("a")
        self.b_sym = Symbol("b")
        self.c_sym = Symbol("c")

        # Propositions
        self.a = AtomicFormula(self.a_sym)
        self.b = AtomicFormula(self.b_sym)
        self.c = AtomicFormula(self.c_sym)
        self.alphabet = Alphabet({self.a_sym, self.b_sym, self.c_sym})

        self.ref = REf(self.alphabet)
        self.trace_1_list = [
            {self.a, self.b},
            {self.a, self.c},
            {self.a, self.b},
            {self.a, self.c},
            {self.b, self.c},
        ]
        self.trace_1 = FiniteTrace(self.trace_1_list, self.alphabet)


    def test_truth_propositional(self):
        ref = self.ref
        a = self.a
        b = self.b
        c = self.c
        self.assertTrue(ref.truth(a, self.trace_1, 0, 1))
        self.assertTrue(ref.truth(And(Not(b), And(a, c)), self.trace_1, 1, 2))
        self.assertFalse(ref.truth(And(b, And(a, c)), self.trace_1, 1, 2))
        self.assertTrue(ref.truth(TrueFormula(), self.trace_1, 0, 1))
        self.assertFalse(ref.truth(FalseFormula(), self.trace_1, 0, 1))
        self.assertFalse(ref.truth(TrueFormula(), self.trace_1, 0, 5))
        self.assertFalse(ref.truth(TrueFormula(), self.trace_1, 0, 0))

    def test_truth_union(self):
        ref = self.ref
        a = self.a
        b = self.b
        c = self.c
        self.assertTrue(ref.truth(PathExpressionUnion(a, b), self.trace_1, 0, 1))
        self.assertTrue(ref.truth(PathExpressionUnion(a, c), self.trace_1, 4, 5))
        self.assertFalse(ref.truth(PathExpressionUnion(Not(b), Not(c)), self.trace_1, 4, 5))

    def test_truth_sequence(self):
        ref = self.ref
        a = self.a
        b = self.b
        c = self.c
        self.assertTrue(ref.truth(PathExpressionSequence(And(a, b), And(a, c)), self.trace_1, 0, 2))
        self.assertTrue(ref.truth(PathExpressionSequence(And(a, b), PathExpressionSequence(And(a, c), And(b, c))), self.trace_1, 2, 5))

    def test_truth_star(self):
        ref = self.ref
        a = self.a
        b = self.b
        c = self.c
        self.assertTrue(ref.truth(PathExpressionStar(a), self.trace_1, 0, 4))
        self.assertFalse(ref.truth(PathExpressionStar(a), self.trace_1, 0, 5))
        self.assertTrue(ref.truth(PathExpressionStar(Or(a, Or(b, c))), self.trace_1, 0, 5))
        self.assertTrue(ref.truth(TrueFormula(), self.trace_1, 0, 1))

