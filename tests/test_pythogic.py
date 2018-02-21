#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythogic` package."""

import unittest

from pythogic.fol.semantics.Interpretation import Interpretation
from pythogic.fol.semantics.Relation import Relation
from pythogic.fol.syntax.Symbol import Symbol, ConstantSymbol, FunctionSymbol, PredicateSymbol
from pythogic.fol.syntax.Term import Variable, FunctionTerm, ConstantTerm
from pythogic.fol.syntax.Formula import PredicateFormula, Equal, Negate, And, Or, Implies, Exists, ForAll
from pythogic.fol.syntax.FOL import FOL


class TestPythogic(unittest.TestCase):
    """Tests for `pythogic` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""


class TestSyntax(TestPythogic):
    """Tests for `pythogic.syntax` package."""

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
        self.A_a = PredicateFormula(self.A, self.a)
        self.a_equal_a = Equal(self.a, self.a)
        self.b_equal_c = Equal(self.b, self.c)
        self.neg_a_equal_a = Negate(self.a_equal_a)
        self.neg_Aa = Negate(self.A_a)
        self.Aa_and_b_equal_c = And(self.A_a, self.b_equal_c)
        self.Aa_or_b_equal_c = Or(self.A_a, self.b_equal_c)
        self.Aa_implies_b_equal_c = Implies(self.A_a, self.b_equal_c)
        self.exists_a_predicate_ab = Exists(self.a, self.predicate_ab)
        self.forall_b_exists_a_predicate_ab = ForAll(self.b, self.exists_a_predicate_ab)

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

        self.dummy_predicate = PredicateFormula(self.dummy_predicate_sym, self.a, self.b)
        self.dummy_predicate_only_one_symbol_false = PredicateFormula(self.predicate_sym, self.a, self.dummy_variable)
        self.dummy_equal = Equal(self.c, self.dummy_variable)
        self.dummy_neg = Negate(self.dummy_predicate_only_one_symbol_false)
        self.dummy_and = And(self.dummy_predicate, self.predicate_ab)
        self.dummy_or = Or(self.dummy_predicate_only_one_symbol_false, self.predicate_ac)

        self.dummy_exists = Exists(self.dummy_variable, self.dummy_predicate_only_one_symbol_false)
        self.dummy_forall = ForAll(self.b, self.dummy_predicate)

    def tearDown(self):
        pass

    def test_str(self):
        """Test __str__() methods"""
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
        self.assertEqual(str(self.predicate_ab), "Predicate^2(a, b)")
        self.assertEqual(str(self.predicate_ac), "Predicate^2(a, c)")
        self.assertEqual(str(self.a_equal_a), "a = a")
        self.assertEqual(str(self.b_equal_c), "b = c")
        self.assertEqual(str(self.neg_a_equal_a), "~(a = a)")
        self.assertEqual(str(self.neg_Aa), "~(A^1(a))")
        self.assertEqual(str(self.Aa_and_b_equal_c), "A^1(a) & b = c")
        self.assertEqual(str(self.Aa_or_b_equal_c), "A^1(a) | b = c")
        self.assertEqual(str(self.Aa_implies_b_equal_c), "A^1(a) >> b = c")
        self.assertEqual(str(self.exists_a_predicate_ab), "∃a.Predicate^2(a, b)")
        self.assertEqual(str(self.forall_b_exists_a_predicate_ab), "Ɐb.∃a.Predicate^2(a, b)")

    def test_eq(self):
        # Symbols
        self.assertEqual(self.a_sym, self.a_sym)
        self.assertEqual(self.a_sym, Symbol("a"))
        self.assertEqual(self.const_sym, ConstantSymbol("Const"))
        self.assertEqual(self.fun_sym, FunctionSymbol("Fun", 3))
        self.assertEqual(self.predicate_sym, PredicateSymbol("Predicate", 2))

        self.assertNotEqual(self.a_sym, Symbol("c"))
        self.assertNotEqual(self.const_sym, ConstantSymbol("Another_Const"))
        self.assertNotEqual(self.fun_sym, FunctionSymbol("Another_Fun", 3))
        self.assertNotEqual(self.fun_sym, FunctionSymbol("Fun", 2))
        self.assertNotEqual(self.predicate_sym, PredicateSymbol("Another_Predicate", 2))
        self.assertNotEqual(self.predicate_sym, PredicateSymbol("Predicate", 1))

        self.assertNotEqual(self.a_sym, self.fun_sym)
        self.assertNotEqual(self.const_sym, self.fun_sym)

        # Terms
        self.assertEqual(self.a, self.a)
        self.assertEqual(self.a, Variable.fromString("a"))
        self.assertEqual(self.const, ConstantTerm(ConstantSymbol("Const")))
        self.assertEqual(self.fun_abc, FunctionTerm(FunctionSymbol("Fun", 3), self.a, self.b, self.c))

        self.assertNotEqual(self.a, self.b)
        self.assertNotEqual(self.a, Variable.fromString("c"))
        self.assertNotEqual(self.const, ConstantTerm(ConstantSymbol("Another_Const")))
        self.assertNotEqual(self.fun_abc, FunctionTerm(FunctionSymbol("Another_Fun", 3), self.a, self.b, self.c))
        self.assertNotEqual(self.fun_abc, FunctionTerm(FunctionSymbol("Fun", 3), self.a, self.b, self.a))

        self.assertNotEqual(self.a, self.fun_abc)

        # Formulas
        self.assertEqual(self.predicate_ab, PredicateFormula(PredicateSymbol("Predicate", 2), Variable.fromString("a"),
                                                             Variable.fromString("b")))
        self.assertEqual(self.A_a, PredicateFormula(PredicateSymbol("A", 1), Variable.fromString("a")))
        self.assertEqual(self.b_equal_c, Equal(Variable.fromString("b"), Variable.fromString("c")))
        self.assertEqual(self.neg_a_equal_a, Negate(Equal(Variable.fromString("a"), Variable.fromString("a"))))
        self.assertEqual(self.forall_b_exists_a_predicate_ab,
                         ForAll(Variable.fromString("b"), Exists(Variable.fromString("a"),
                                                                 PredicateFormula(PredicateSymbol("Predicate", 2),
                                                                                  Variable.fromString("a"),
                                                                                  Variable.fromString("b")))))

        self.assertNotEqual(self.predicate_ab,
                            PredicateFormula(PredicateSymbol("Predicate", 2), Variable.fromString("a"),
                                             Variable.fromString("c")))
        self.assertNotEqual(self.predicate_ab,
                            PredicateFormula(PredicateSymbol("Another_Predicate", 2), Variable.fromString("a"),
                                             Variable.fromString("c")))
        self.assertNotEqual(self.A_a, PredicateFormula(PredicateSymbol("A", 1), Variable.fromString("b")))
        self.assertNotEqual(self.b_equal_c, Equal(Variable.fromString("b"), Variable.fromString("b")))
        self.assertNotEqual(self.neg_a_equal_a, Negate(Equal(Variable.fromString("b"), Variable.fromString("a"))))
        self.assertNotEqual(self.forall_b_exists_a_predicate_ab,
                            ForAll(Variable.fromString("b"), Exists(Variable.fromString("a"),
                                                                    PredicateFormula(
                                                                        PredicateSymbol("ANOTHER_PREDICATE", 2),
                                                                        Variable.fromString("a"),
                                                                        Variable.fromString("b")))))

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
        """Test if FOL._is_formula() works correctly"""

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
        self.assertTrue(self.myFOL._is_formula(self.exists_a_predicate_ab))
        self.assertTrue(self.myFOL._is_formula(self.forall_b_exists_a_predicate_ab))

        # using illegal formulas
        self.assertFalse(self.myFOL._is_formula(self.dummy_predicate))
        self.assertFalse(self.myFOL._is_formula(self.dummy_predicate_only_one_symbol_false))
        self.assertFalse(self.myFOL._is_formula(self.dummy_equal))
        self.assertFalse(self.myFOL._is_formula(self.dummy_neg))
        self.assertFalse(self.myFOL._is_formula(self.dummy_and))

    def test_containsVariable(self):
        """Test if Formula.containsVariable works correctly"""

        # using the same objects
        self.assertTrue(self.predicate_ab.containsVariable(self.a))
        self.assertTrue(self.predicate_ab.containsVariable(self.b))
        self.assertTrue(self.A_a.containsVariable(self.a))
        self.assertTrue(self.A_a.containsVariable(self.a))
        self.assertTrue(self.a_equal_a.containsVariable(self.a))
        self.assertTrue(self.b_equal_c.containsVariable(self.c))
        self.assertTrue(self.neg_a_equal_a.containsVariable(self.a))
        self.assertTrue(self.neg_Aa.containsVariable(self.a))
        self.assertTrue(self.Aa_and_b_equal_c.containsVariable(self.c))
        self.assertTrue(self.Aa_or_b_equal_c.containsVariable(self.a))
        self.assertTrue(self.Aa_or_b_equal_c.containsVariable(self.c))
        self.assertTrue(self.Aa_or_b_equal_c.containsVariable(self.c))

        self.assertFalse(self.predicate_ab.containsVariable(self.c))

        # using different objects
        new_a = Variable.fromString("a")
        new_b = Variable.fromString("b")
        self.assertTrue(self.predicate_ab.containsVariable(new_a))
        self.assertTrue(self.predicate_ab.containsVariable(new_b))


class TestSemantics(TestPythogic):
    """Tests for `pythogic.semantics` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.objects = {"john", "paul", "george", "joseph"}
        self.Person = Relation("Person", 2, {("john", 20), ("paul", 21), ("george", 22), ("joseph", 23)})

        self.I = Interpretation.fromRelationsAndFunctions({self.Person},set())



    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_(self):
        pass
