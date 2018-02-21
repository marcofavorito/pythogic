#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythogic` package."""


import unittest

from pythogic import pythogic
from pythogic.fol import Symbol, Variable, FunctionTerm, ConstantSymbol, FunctionSymbol, PredicateSymbol, ConstantTerm


class TestPythogic(unittest.TestCase):
    """Tests for `pythogic` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""



class TestFol(TestPythogic):
    """Tests for `fol` module """

    def setUp(self):
        self.a_sym = Symbol('a')
        self.b_sym = Symbol('b')
        self.const_sym = ConstantSymbol("const")
        self.fun_sym = FunctionSymbol("fun", 3)
        self.predicate_sym = PredicateSymbol("predicate", 2)

        self.a = Variable(self.a_sym)
        self.b = Variable(self.b_sym)
        self.c = Variable.fromString("c")
        self.const = ConstantTerm(self.const_sym)
        self.fun_abc = FunctionTerm(self.fun_sym, self.a, self.b, self.c)
        # self.predicate_ab = PredicateTerm(self.predicate_sym, self.a, self.b)
        # self.predicate_ac = PredicateTerm(self.predicate_sym, self.a, self.c)


    def tearDown(self):
        pass


    def test_str(self):
        # Symbols
        unittest.TestCase.assertEqual(self, str(self.a_sym), "a")
        unittest.TestCase.assertEqual(self, str(self.const_sym), "const^0")
        unittest.TestCase.assertEqual(self, str(self.fun_sym), "fun^3")
        unittest.TestCase.assertEqual(self, str(self.predicate_sym), "predicate^2")

        # Terms
        unittest.TestCase.assertEqual(self, str(self.a), "a")
        unittest.TestCase.assertEqual(self, str(self.c), "c")
        unittest.TestCase.assertEqual(self, str(self.const), "const^0()")
        unittest.TestCase.assertEqual(self, str(self.fun_abc), "fun^3(a, b, c)")
        # unittest.TestCase.assertEqual(self, str(self.predicate_ab), "predicate^2(a, b)")
        # unittest.TestCase.assertEqual(self, str(self.predicate_ac), "predicate^2(a, c)")

    def test_(self):
        pass


