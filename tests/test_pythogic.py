#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythogic` package."""


import unittest

from pythogic.fol.Symbol import Symbol, ConstantSymbol, FunctionSymbol, PredicateSymbol
from pythogic.fol.fol import Variable, ConstantTerm, FunctionTerm, PredicateFormula, Equal, Negate, And, Or, Implies, \
    FOL


class TestPythogic(unittest.TestCase):
    """Tests for `pythogic` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""



class TestFol(TestPythogic):
    """Tests for `fol` module """

    def setUp(self):
        """Set up symbols, terms and formulas. Both legal and illegal, according to some FOL system"""

        # Symbols
        self.a_sym = Symbol('a')
        self.b_sym = Symbol('b')
        self.const_sym = ConstantSymbol("Const")
        self.fun_sym = FunctionSymbol("Fun", 3)
        self.predicate_sym = PredicateSymbol("Predicate", 2)
        self.A = PredicateSymbol("A", 1)

        # Terms
        self.a = Variable(self.a_sym)
        self.b = Variable(self.b_sym)
        self.c = Variable.fromString("c")
        self.const = ConstantTerm(self.const_sym)
        self.fun_abc = FunctionTerm(self.fun_sym, self.a, self.b, self.c)

        # Formulas
        self.predicate_ab = PredicateFormula(self.predicate_sym, self.a, self.b)
        self.predicate_ac = PredicateFormula(self.predicate_sym, self.a, self.c)
        self.A_a          = PredicateFormula(self.A, self.a)
        self.a_equal_a = Equal(self.a, self.a)
        self.b_equal_c = Equal(self.b, self.c)
        self.neg_a_equal_a = Negate(self.a_equal_a)
        self.neg_Aa = Negate(self.A_a)
        self.Aa_and_b_equal_c = And(self.A_a, self.b_equal_c)
        self.Aa_or_b_equal_c = Or(self.A_a, self.b_equal_c)
        self.Aa_implies_b_equal_c = Implies(self.A_a, self.b_equal_c)

        # FOL
        self.vars = {self.a, self.b, self.c}
        self.functions = {self.const_sym, self.fun_sym}
        self.predicates = {self.predicate_sym, self.A}

        self.myFOL = FOL(self.vars, self.functions, self.predicates)

        # define dummy stuff
        # does not belong to myFOL. They are used for test membership to myFOL
        self.dummy_variable = Variable.fromString("ThisVariableDoesNotBelongToFOLSystem")
        self.dummy_fun_sym = FunctionSymbol("ThisFunctionDoesNotBelongToFOLSystem", 3)
        self.dummy_constant_sym = ConstantSymbol("ThisConstDoesNotBelongToFOLSystem")
        self.dummy_predicate_sym = PredicateSymbol("ThisPredicateDoesNotBelongToFOLSystem", 2)

        self.dummy_fun = FunctionTerm(self.dummy_fun_sym, self.a, self.b, self.dummy_variable)
        self.dummy_constant = ConstantTerm(self.dummy_constant_sym)

        self.dummy_predicate = PredicateFormula(self.dummy_predicate_sym, self.a, self.dummy_variable)
        self.dummy_predicate_only_one_symbol_false = PredicateFormula(self.predicate_sym, self.a, self.dummy_variable)
        self.dummy_equal = Equal(self.c, self.dummy_variable)
        self.dummy_neg = Negate(self.dummy_variable)
        self.dummy_and = And(self.dummy_predicate_only_one_symbol_false, self.predicate_ab)



    def tearDown(self):
        pass


    def test_str(self):
        # Symbols
        self.assertEqual(str(self.a_sym), "a")
        self.assertEqual(str(self.const_sym), "Const^0")
        self.assertEqual(str(self.fun_sym), "Fun^3")
        self.assertEqual(str(self.predicate_sym), "Predicate^2")

        # Terms
        self.assertEqual(str(self.a), "a")
        self.assertEqual(str(self.c), "c")
        self.assertEqual(str(self.const), "Const^0()")
        self.assertEqual(str(self.fun_abc), "Fun^3(a, b, c)")

        # Formulas
        self.assertEqual(str(self.predicate_ab),          "Predicate^2(a, b)")
        self.assertEqual(str(self.predicate_ac),          "Predicate^2(a, c)")
        self.assertEqual(str(self.a_equal_a),             "a = a")
        self.assertEqual(str(self.b_equal_c),             "b = c")
        self.assertEqual(str(self.neg_a_equal_a),         "~(a = a)")
        self.assertEqual(str(self.neg_Aa),                "~(A^1(a))")
        self.assertEqual(str(self.Aa_and_b_equal_c),      "A^1(a) & b = c")
        self.assertEqual(str(self.Aa_or_b_equal_c),       "A^1(a) | b = c")
        self.assertEqual(str(self.Aa_implies_b_equal_c),  "A^1(a) >> b = c")





    def test_is_term(self):
        """Test if FOL._is_term() works correctly"""

        # using legal terms
        self.assertTrue(self.myFOL._is_term(self.a))
        self.assertTrue(self.myFOL._is_term(self.c))
        self.assertTrue(self.myFOL._is_term(self.const))
        self.assertTrue(self.myFOL._is_term(self.fun_abc))

        # using illegal terms
        self.assertFalse(self.myFOL._is_term(self.dummy_variable))
        self.assertFalse(self.myFOL._is_term(self.dummy_constant))
        self.assertFalse(self.myFOL._is_term(self.dummy_fun))



    def test_is_formula(self):
        """Test if FOL._is_formula() work correctly"""

        # using legal formulas
        self.assertTrue(self.myFOL._is_formula(self.predicate_ab))
        self.assertTrue(self.myFOL._is_formula(self.A_a))
        self.assertTrue(self.myFOL._is_formula(self.a_equal_a))
        self.assertTrue(self.myFOL._is_formula(self.b_equal_c))
        self.assertTrue(self.myFOL._is_formula(self.neg_a_equal_a))
        self.assertTrue(self.myFOL._is_formula(self.neg_Aa))
        self.assertTrue(self.myFOL._is_formula(self.Aa_and_b_equal_c))
        self.assertTrue(self.myFOL._is_formula(self.Aa_or_b_equal_c))
        self.assertTrue(self.myFOL._is_formula(self.Aa_implies_b_equal_c))


        # using illegal formulas
        self.assertFalse(self.myFOL._is_formula(self.dummy_predicate))
        self.assertFalse(self.myFOL._is_formula(self.dummy_predicate_only_one_symbol_false))
        self.assertFalse(self.myFOL._is_formula(self.dummy_equal))
        self.assertFalse(self.myFOL._is_formula(self.dummy_neg))
        self.assertFalse(self.myFOL._is_formula(self.dummy_and))





