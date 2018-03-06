#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythogic` package."""

import unittest

from pythogic.fol.semantics.Assignment import Assignment
from pythogic.fol.semantics.Function import Function
from pythogic.fol.semantics.Interpretation import Interpretation
from pythogic.fol.semantics.Relation import Relation
from pythogic.fol.syntax.FOLAlphabet import FOLAlphabet
from pythogic.base.Symbol import Symbol, ConstantSymbol, FunctionSymbol, PredicateSymbol
from pythogic.fol.syntax.Term import Variable, FunctionTerm, ConstantTerm
from pythogic.base.Formula import PredicateFormula, Equal, Not, And, Or, Implies, Exists, ForAll, Equivalence, \
    TrueFormula, FalseFormula, DUMMY_TERM
from pythogic.fol.FOL import FOL


class TestFOL(unittest.TestCase):
    """Tests for `pythogic.fol` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""


class TestFOLSyntax(TestFOL):
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
        self.neg_a_equal_a = Not(self.a_equal_a)
        self.neg_Aa = Not(self.A_a)
        self.Aa_and_b_equal_c = And(self.A_a, self.b_equal_c)
        self.Aa_or_b_equal_c = Or(self.A_a, self.b_equal_c)
        self.Aa_implies_b_equal_c = Implies(self.A_a, self.b_equal_c)
        self.exists_a_predicate_ab = Exists(self.a, self.predicate_ab)
        self.forall_b_exists_a_predicate_ab = ForAll(self.b, self.exists_a_predicate_ab)

        # FOL
        self.vars = {self.a, self.b, self.c}
        self.functions = {self.const_sym, self.fun_sym}
        self.predicates = {self.predicate_sym, self.A}

        self.alphabet = FOLAlphabet(self.functions, self.predicates)
        self.myFOL = FOL(self.alphabet)

        # define dummy stuff
        # does not belong to myFOL. They are used for test membership to myFOL
        self.dummy_variable = Variable.fromString("ThisVariableDoesNotBelongToFOLSystem")
        self.dummy_fun_sym = FunctionSymbol("ThisFunctionDoesNotBelongToFOLSystem", 3)
        self.dummy_constant_sym = ConstantSymbol("ThisConstDoesNotBelongToFOLSystem")
        self.dummy_predicate_sym = PredicateSymbol("ThisPredicateDoesNotBelongToFOLSystem", 2)

        self.dummy_fun = FunctionTerm(self.dummy_fun_sym, self.a, self.b, self.dummy_variable)
        self.dummy_constant = ConstantTerm(self.dummy_constant_sym)

        self.dummy_predicate = PredicateFormula(self.dummy_predicate_sym, self.a, self.b)
        self.dummy_predicate_only_one_symbol_false = PredicateFormula(self.predicate_sym, self.dummy_variable, self.dummy_constant)
        self.dummy_equal = Equal(self.c, self.dummy_constant)
        self.dummy_neg = Not(self.dummy_predicate_only_one_symbol_false)
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
        self.assertEqual(str(self.Aa_and_b_equal_c), "(A^1(a) & b = c)")
        self.assertEqual(str(self.Aa_or_b_equal_c), "(A^1(a) | b = c)")
        self.assertEqual(str(self.Aa_implies_b_equal_c), "(A^1(a) >> b = c)")
        self.assertEqual(str(self.exists_a_predicate_ab), "∃a.(Predicate^2(a, b))")
        self.assertEqual(str(self.forall_b_exists_a_predicate_ab), "Ɐb.(∃a.(Predicate^2(a, b)))")

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
        self.assertEqual(self.predicate_ab, PredicateFormula(PredicateSymbol("Predicate", 2),
                                                             Variable.fromString("a"), Variable.fromString("b")))
        self.assertEqual(self.A_a, PredicateFormula(PredicateSymbol("A", 1),
                                                    Variable.fromString("a")))
        self.assertEqual(self.b_equal_c, Equal(Variable.fromString("b"), Variable.fromString("c")))
        self.assertEqual(self.neg_a_equal_a, Not(Equal(Variable.fromString("a"), Variable.fromString("a"))))
        self.assertEqual(self.forall_b_exists_a_predicate_ab,
                         ForAll(Variable.fromString("b"),
                                Exists(Variable.fromString("a"),
                                       PredicateFormula(PredicateSymbol("Predicate", 2),
                                                        Variable.fromString("a"),
                                                        Variable.fromString("b")))))

        self.assertNotEqual(self.predicate_ab,
                            PredicateFormula(PredicateSymbol("Predicate", 2),
                                             Variable.fromString("a"),
                                             Variable.fromString("c")))
        self.assertNotEqual(self.predicate_ab,
                            PredicateFormula(PredicateSymbol("Another_Predicate", 2),
                                             Variable.fromString("a"),
                                             Variable.fromString("c")))
        self.assertNotEqual(self.A_a, PredicateFormula(PredicateSymbol("A", 1), Variable.fromString("b")))
        self.assertNotEqual(self.b_equal_c, Equal(Variable.fromString("b"), Variable.fromString("b")))
        self.assertNotEqual(self.neg_a_equal_a, Not(Equal(Variable.fromString("b"), Variable.fromString("a"))))
        self.assertNotEqual(self.forall_b_exists_a_predicate_ab,
                            ForAll(Variable.fromString("b"),
                                   Exists(Variable.fromString("a"),
                                          PredicateFormula(PredicateSymbol("ANOTHER_PREDICATE", 2),
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
        self.assertFalse(self.myFOL._is_term(self.dummy_constant))
        self.assertFalse(self.myFOL._is_term(self.dummy_fun))

    def test_is_formula(self):
        """Test if FOL._is_formula() works correctly"""

        # using legal formulas
        self.assertTrue(self.myFOL.is_formula(self.predicate_ab))
        self.assertTrue(self.myFOL.is_formula(self.A_a))
        self.assertTrue(self.myFOL.is_formula(self.a_equal_a))
        self.assertTrue(self.myFOL.is_formula(self.b_equal_c))
        self.assertTrue(self.myFOL.is_formula(self.neg_a_equal_a))
        self.assertTrue(self.myFOL.is_formula(self.neg_Aa))
        self.assertTrue(self.myFOL.is_formula(self.Aa_and_b_equal_c))
        self.assertTrue(self.myFOL.is_formula(self.Aa_or_b_equal_c))
        self.assertTrue(self.myFOL.is_formula(self.Aa_implies_b_equal_c))
        self.assertTrue(self.myFOL.is_formula(self.exists_a_predicate_ab))
        self.assertTrue(self.myFOL.is_formula(self.forall_b_exists_a_predicate_ab))

        # using illegal formulas (something that is not in the alphabet of the FOL)
        self.assertFalse(self.myFOL.is_formula(self.dummy_predicate))
        self.assertFalse(self.myFOL.is_formula(self.dummy_predicate_only_one_symbol_false))
        self.assertFalse(self.myFOL.is_formula(self.dummy_equal))
        self.assertFalse(self.myFOL.is_formula(self.dummy_neg))
        self.assertFalse(self.myFOL.is_formula(self.dummy_and))

class TestFOLSemantics(TestFOL):
    """Tests for `pythogic.semantics` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

        self.Person_pred_sym = PredicateSymbol("Person", 2)
        self.Lives_pred_sym = PredicateSymbol("Lives", 2)
        self.LivesIn_fun_sym = FunctionSymbol("LivesIn", 1)

        self.objects = {"john", "paul", "george", "joseph"}
        self.person_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 23)}
        self.lives_tuples  = {("john", "ny"), ("paul", "london"), ("george", "paris"), ("joseph", "paris")}

        self.livesin_function_dictionary = {
            ("john",)  : "ny",
            ("paul",)  : "london",
            ("george",): "paris",
            ("joseph",): "paris"
        }

        self.Person = Relation(self.Person_pred_sym, self.person_tuples)
        self.Lives = Relation(self.Lives_pred_sym, self.lives_tuples)
        self.LivesIn = Function(self.LivesIn_fun_sym, self.livesin_function_dictionary)


        self.I = Interpretation.fromRelationsAndFunctions({self.LivesIn}, {self.Person, self.Lives})
        self.alphabet = self.I.alphabet
        self.FOL = FOL(self.alphabet)

        self.x = Variable.fromString("x")
        self.y = Variable.fromString("y")
        self.z = Variable.fromString("z")
        self.var2obj = {
            self.x: "john",
            self.y: 20,
            self.z: "ny"
        }

        self.assignment = Assignment(self.var2obj, self.I)




    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_relation_eq(self):
        relation = Relation(PredicateSymbol("Predicate", 1), {("string_1", ), ("string_2",), ("string_3", )})
        the_same_relation = Relation(PredicateSymbol("Predicate", 1), {("string_1", ), ("string_2",), ("string_3", )})
        the_same_relation_but_different_symbol = Relation(PredicateSymbol("Another_Predicate", 1), {("string_1", ), ("string_2",), ("string_3", )})
        the_same_relation_but_different_tuples = Relation(PredicateSymbol("Predicate", 1), {("string_1",), ("string_2",), ("different_string_3",)})

        self.assertEqual(relation, the_same_relation)
        self.assertNotEqual(relation, "NotARelation")
        self.assertNotEqual(relation, the_same_relation_but_different_symbol)
        self.assertNotEqual(relation, the_same_relation_but_different_tuples)
        # Test hash
        self.assertEqual(len({self.LivesIn}), len({self.LivesIn, self.LivesIn}))

    def test_function_eq(self):
        function = Function(FunctionSymbol("Function", 1), {("string_1",) : 1, ("string_2", ): 2, ("string_3",):3})
        the_same_function = Function(FunctionSymbol("Function", 1), {("string_1",) : 1, ("string_2", ): 2, ("string_3",):3} )
        the_same_function_different_order = Function(FunctionSymbol("Function", 1),{("string_2",): 2, ("string_3",): 3, ("string_1",): 1})
        the_same_function_but_different_symbol = Function(FunctionSymbol("Another_Function", 1), {("string_1",): 1, ("string_2",): 2, ("string_3",): 3})
        the_same_function_but_different_values = Function(FunctionSymbol("Function", 1), {("string_1",): 1, ("string_2",): 2, ("string_3",): 4})

        self.assertEqual(function, the_same_function)
        self.assertEqual(function, the_same_function_different_order)
        self.assertNotEqual(function, "NotAFunction")
        self.assertNotEqual(function, the_same_function_but_different_symbol)
        self.assertNotEqual(function, the_same_function_but_different_values)


    def test_relation_getter(self):
        the_same_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 23)}
        different_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 20)}

        the_same_relation = Relation(PredicateSymbol("Person", 2), the_same_tuples)
        the_same_relation_but_different_symbol = Relation(PredicateSymbol("Another_Person", 2), the_same_tuples)
        the_same_relation_but_different_tuples = Relation(PredicateSymbol("Person", 2), different_tuples)

        self.assertEqual(self.I.getRelation(self.Person_pred_sym), the_same_relation)
        self.assertNotEqual(self.I.getRelation(self.Person_pred_sym), the_same_relation_but_different_symbol)
        self.assertNotEqual(self.I.getRelation(self.Person_pred_sym), the_same_relation_but_different_tuples)

    def test_function_getter(self):
        the_same_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 23)}
        different_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 20)}

        the_same_function = Relation(PredicateSymbol("Person", 2), the_same_tuples)
        the_same_function_but_different_symbol = Relation(PredicateSymbol("Another_Person", 2), the_same_tuples)
        the_same_function_but_different_tuples = Relation(PredicateSymbol("Person", 2), different_tuples)

        self.assertEqual(self.I.getRelation(self.Person_pred_sym), the_same_function)
        self.assertNotEqual(self.I.getRelation(self.Person_pred_sym), the_same_function_but_different_symbol)
        self.assertNotEqual(self.I.getRelation(self.Person_pred_sym), the_same_function_but_different_tuples)

    def test_interpretation_fromRelationsAndFunctions(self):
        actual_domain = {
            "john", "paul", "george", "joseph",
            20, 21, 22, 23,
            "ny", "london", "paris"
        }
        actual_constants = {Function(ConstantSymbol(str(e)), {():e}) for e in actual_domain}
        actual_functions_plus_constants = actual_constants.union({self.LivesIn})
        actual_relations = {self.Lives,self.Person}

        self.assertEqual(self.I.domain, actual_domain)
        self.assertEqual(self.I.functions, actual_functions_plus_constants)
        self.assertEqual(self.I.relations, actual_relations)

    def test_assignment(self):
        self.assertEqual(self.assignment(self.x), "john")
        self.assertEqual(self.assignment(self.y), 20)
        self.assertEqual(self.assignment(self.z), "ny")

        self.assertEqual(self.assignment(FunctionTerm(self.LivesIn_fun_sym, self.x)), "ny")
        self.assertTrue((self.assignment(self.x), self.assignment(ConstantTerm.fromString("20"))) in self.Person.tuples)

    def test_truth(self):
        w = Variable.fromString("w")
        Person_x_20 = PredicateFormula(self.Person_pred_sym, self.x, ConstantTerm.fromString("20"))
        Person_x_y = PredicateFormula(self.Person_pred_sym, self.x, self.y)
        not_Person_x_21 = Not(PredicateFormula(self.Person_pred_sym, self.x, ConstantTerm.fromString("21")))
        y_equal_20 = Equal(self.y, ConstantTerm.fromString("20"))
        x_equal_john = Equal(self.x, ConstantTerm.fromString("john"))
        x_equal_x = Equal(self.x, self.x)
        x_equal_y = Equal(self.x, self.y)
        x_equal_z = Equal(self.x, self.z)

        x_lives_w = PredicateFormula(self.Lives_pred_sym, self.x, w)
        x_lives_y = PredicateFormula(self.Lives_pred_sym, self.x, self.y)
        x_lives_ny = PredicateFormula(self.Lives_pred_sym, self.x, ConstantTerm.fromString("ny"))
        x_lives_paris = PredicateFormula(self.Lives_pred_sym, self.x, ConstantTerm.fromString("paris"))
        w_lives_z = PredicateFormula(self.Lives_pred_sym, w, self.z)

        exists_w__x_lives_w = Exists(w, x_lives_w)
        exists_y__x_lives_y = Exists(self.y, x_lives_y)
        exists_z_exists_w__w_lives_z = Exists(self.z, Exists(w, w_lives_z))
        exists_x__x_equal_x = Exists(self.x, x_equal_x)
        exists_x__x_equal_y = Exists(self.x, x_equal_y)
        exists_x__x_equal_john_and_Lives_x_paris = Exists(self.x, And(x_equal_john, x_lives_paris))
        exists_x__x_equal_john_and_exists_x__Lives_x_ny = And(Exists(self.x, x_equal_john), Exists(self.x, x_lives_ny))
        exists_x__x_equal_x_and_exists_x__Lives_x_ny = And(exists_x__x_equal_x, Exists(self.x, x_lives_ny))

        forall_x__x_equal_x = ForAll(self.x, x_equal_x)
        forall_x__x_equal_y = ForAll(self.x, x_equal_y)
        not_forall_x__x_equal_x  = Not(forall_x__x_equal_x)

        # Person(x, 20)
        # x = "john"
        self.assertTrue(self.FOL.truth(Person_x_20, self.assignment))

        # ~Person(x, 21)
        # x = "john"
        self.assertTrue(self.FOL.truth(not_Person_x_21, self.assignment))

        # Equals
        self.assertTrue(self.FOL.truth(y_equal_20, self.assignment))
        self.assertTrue(self.FOL.truth(x_equal_x, self.assignment))
        self.assertFalse(self.FOL.truth(x_equal_y, self.assignment))
        self.assertFalse(self.FOL.truth(x_equal_z, self.assignment))

        # y == 20 and x == "john" and Person(x, y)
        self.assertTrue(self.FOL.truth(And(y_equal_20, And(x_equal_john, Person_x_y)), self.assignment))

        self.assertTrue(self.FOL.truth(Or(Person_x_20, x_equal_john), self.assignment))
        # De Morgan on previous formula
        # Not (Not y == 20 or Not x == "john" ot Not Person(x, y)
        self.assertTrue(self.FOL.truth(Not(Or(Not(y_equal_20), Or(Not(x_equal_john), Not(Person_x_y)))), self.assignment))

        # Or with the last formula true
        self.assertTrue(self.FOL.truth(Or(Equal(self.x, self.y), Or(Equal(self.x, self.y), Equal(self.z,self.z))), self.assignment))

        # (y==20 and x=="john") => Person(x,y)
        self.assertTrue(self.FOL.truth(Implies(And(y_equal_20, x_equal_john), Person_x_y), self.assignment))

        self.assertTrue(self.FOL.truth(Implies(Not(x_equal_x), Person_x_y), self.assignment))

        # Exists
        self.assertTrue(self.FOL.truth(exists_w__x_lives_w, self.assignment))
        self.assertTrue(self.FOL.truth(exists_x__x_equal_x, self.assignment))
        self.assertTrue(self.FOL.truth(exists_x__x_equal_y, self.assignment))
        # quantified variable not present in the formula
        self.assertTrue(self.FOL.truth(exists_y__x_lives_y, self.assignment))
        # 2 quantified variables
        self.assertTrue(self.FOL.truth(exists_z_exists_w__w_lives_z, self.assignment))
        # annidate exists
        self.assertTrue(self.FOL.truth(exists_x__x_equal_john_and_exists_x__Lives_x_ny, self.assignment))
        self.assertTrue(self.FOL.truth(exists_x__x_equal_x_and_exists_x__Lives_x_ny, self.assignment))
        self.assertFalse(self.FOL.truth(exists_x__x_equal_john_and_Lives_x_paris, self.assignment))

        # ForAll
        self.assertTrue(self.FOL.truth(forall_x__x_equal_x, self.assignment))
        self.assertFalse(self.FOL.truth(forall_x__x_equal_y, self.assignment))
        self.assertFalse(self.FOL.truth(not_forall_x__x_equal_x, self.assignment))


class TestFOLIsFormula(TestFOL):
    def setUp(self):
        self.Person_pred_sym = PredicateSymbol("Person", 2)
        self.Lives_pred_sym = PredicateSymbol("Lives", 2)
        self.LivesIn_fun_sym = FunctionSymbol("LivesIn", 1)

        self.objects = {"john", "paul", "george", "joseph"}
        self.person_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 23)}
        self.lives_tuples = {("john", "ny"), ("paul", "london"), ("george", "paris"), ("joseph", "paris")}

        self.livesin_function_dictionary = {
            ("john",): "ny",
            ("paul",): "london",
            ("george",): "paris",
            ("joseph",): "paris"
        }

        self.Person = Relation(self.Person_pred_sym, self.person_tuples)
        self.Lives = Relation(self.Lives_pred_sym, self.lives_tuples)
        self.LivesIn = Function(self.LivesIn_fun_sym, self.livesin_function_dictionary)

        self.I = Interpretation.fromRelationsAndFunctions({self.LivesIn}, {self.Person, self.Lives})
        self.alphabet = self.I.alphabet
        self.fol = FOL(self.alphabet)


    def test_is_formula_predicate(self):
        # TODO: Cover the FunctionTerm case (not only ConstantTerm)
        fol = self.fol
        Person_pred_sym = self.Person_pred_sym
        john = ConstantTerm.fromString("john")
        paul = ConstantTerm.fromString("paul")
        not_a_term = ConstantTerm.fromString("NotATerm")

        # Notice: only syntactic check.
        # test terms
        self.assertTrue(fol.is_formula(PredicateFormula(Person_pred_sym, john, paul)))
        self.assertFalse(fol.is_formula(PredicateFormula(Person_pred_sym, not_a_term, paul)))

        # test predicate symbol
        self.assertTrue(self.fol.is_formula(PredicateFormula(PredicateSymbol("Person", 2), john, paul)))
        self.assertFalse(self.fol.is_formula(PredicateFormula(PredicateSymbol("Person", 3), john, paul, john)))
        self.assertFalse(self.fol.is_formula(PredicateFormula(PredicateSymbol("Person_fake", 2), john, paul)))

    def test_is_formula_equal(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        paul = ConstantTerm.fromString("paul")
        not_a_term = ConstantTerm.fromString("NotATerm")
        right_equal = Equal(john, paul)
        wrong_equal = Equal(john, not_a_term)

        # test terms
        self.assertTrue(fol.is_formula(right_equal))
        self.assertFalse(fol.is_formula(wrong_equal))


    def test_is_formula_not(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        paul = ConstantTerm.fromString("paul")
        not_a_term = ConstantTerm.fromString("NotATerm")
        right_equal = Equal(john, paul)
        wrong_equal = Equal(john, not_a_term)

        self.assertTrue(fol.is_formula(Not(right_equal)))
        self.assertFalse(fol.is_formula(Not(wrong_equal)))

        self.assertTrue(fol.is_formula(Not(PredicateFormula(PredicateSymbol("Person", 2), john, paul))))
        self.assertFalse(fol.is_formula(Not(PredicateFormula(PredicateSymbol("Person", 3), john, paul, john))))
        self.assertFalse(fol.is_formula(Not(PredicateFormula(PredicateSymbol("Person_fake", 2), john, paul))))

    def test_is_formula_and(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        paul = ConstantTerm.fromString("paul")
        not_a_term = ConstantTerm.fromString("NotATerm")
        right_equal = Equal(john, paul)
        wrong_equal = Equal(john, not_a_term)

        self.assertTrue(fol.is_formula(And(right_equal, right_equal)))
        self.assertFalse(fol.is_formula(And(right_equal, Not(wrong_equal))))

        self.assertTrue(fol.is_formula(And(right_equal, PredicateFormula(PredicateSymbol("Person", 2), john, paul))))
        self.assertFalse(fol.is_formula(And(right_equal, PredicateFormula(PredicateSymbol("Person", 3), john, paul, john))))
        self.assertFalse(fol.is_formula(And(right_equal, PredicateFormula(PredicateSymbol("Person_fake", 2), john, paul))))

    def test_is_formula_exists(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        not_a_term = ConstantTerm.fromString("NotATerm")
        x = Variable.fromString("x")
        y = Variable.fromString("y")
        right_equal = Equal(x, john)
        wrong_equal = Equal(x, not_a_term)

        self.assertTrue(fol.is_formula(Exists(x,right_equal)))
        self.assertFalse(fol.is_formula(Exists(x,wrong_equal)))

        self.assertTrue(fol.is_formula(Exists(x, PredicateFormula(PredicateSymbol("Person", 2), john, x))))
        self.assertFalse(fol.is_formula(Exists(x, PredicateFormula(PredicateSymbol("Person", 3), john, x, john))))
        self.assertFalse(fol.is_formula(Exists(x, PredicateFormula(PredicateSymbol("Person_fake", 2), john, x))))
        # self.assertFalse(fol.is_formula(Exists(x, PredicateFormula(PredicateSymbol("Person", 2), john, y))))

    def test_is_formula_derived(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        not_a_term = ConstantTerm.fromString("NotATerm")
        x = Variable.fromString("x")
        y = Variable.fromString("y")
        right_equal = Equal(x, john)
        wrong_equal = Equal(x, not_a_term)

        self.assertTrue(fol.is_formula(TrueFormula()))
        self.assertTrue(fol.is_formula(FalseFormula()))

        self.assertTrue(fol.is_formula(Or(right_equal, right_equal)))
        self.assertFalse(fol.is_formula(Or(right_equal, wrong_equal)))

        self.assertTrue(fol.is_formula(Or(right_equal, right_equal)))
        self.assertFalse(fol.is_formula(Or(right_equal, wrong_equal)))

        self.assertTrue(fol.is_formula(Implies(right_equal, right_equal)))
        self.assertFalse(fol.is_formula(Implies(right_equal, wrong_equal)))

        self.assertTrue(fol.is_formula(Equivalence(right_equal, right_equal)))
        self.assertFalse(fol.is_formula(Equivalence(right_equal, wrong_equal)))

        self.assertTrue(fol.is_formula(ForAll(x, PredicateFormula(PredicateSymbol("Person", 2), john, x))))
        self.assertFalse(fol.is_formula(ForAll(x, PredicateFormula(PredicateSymbol("Person", 3), john, x, john))))
        self.assertFalse(fol.is_formula(ForAll(x, PredicateFormula(PredicateSymbol("Person_fake", 2), john, x))))
        # self.assertFalse(fol.is_formula(ForAll(x, PredicateFormula(PredicateSymbol("Person", 2), john, y))))


class TestFOLExpandFormula(unittest.TestCase):
    def setUp(self):
        self.Person_pred_sym = PredicateSymbol("Person", 2)
        self.Lives_pred_sym = PredicateSymbol("Lives", 2)
        self.LivesIn_fun_sym = FunctionSymbol("LivesIn", 1)

        self.objects = {"john", "paul", "george", "joseph"}
        self.person_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 23)}
        self.lives_tuples = {("john", "ny"), ("paul", "london"), ("george", "paris"), ("joseph", "paris")}

        self.livesin_function_dictionary = {
            ("john",): "ny",
            ("paul",): "london",
            ("george",): "paris",
            ("joseph",): "paris"
        }

        self.Person = Relation(self.Person_pred_sym, self.person_tuples)
        self.Lives = Relation(self.Lives_pred_sym, self.lives_tuples)
        self.LivesIn = Function(self.LivesIn_fun_sym, self.livesin_function_dictionary)

        self.I = Interpretation.fromRelationsAndFunctions({self.LivesIn}, {self.Person, self.Lives})
        self.alphabet = self.I.alphabet
        self.fol = FOL(self.alphabet)

    def test_expand_formula_allowed_formulas(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        x = Variable.fromString("x")
        right_equal = Equal(x, john)
        not_ = Not(right_equal)
        and_ = And(right_equal, not_)
        exists_ = Exists(x, right_equal)

        self.assertEqual(fol.expand_formula(right_equal), right_equal)
        self.assertEqual(fol.expand_formula(not_), not_)
        self.assertEqual(fol.expand_formula(and_), and_)
        self.assertEqual(fol.expand_formula(exists_), exists_)

    def test_expand_formula_derived_formulas(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        x = Variable.fromString("x")
        right_equal = Equal(x, john)
        true_ = TrueFormula()
        false_ = FalseFormula()
        or_ = Or(true_, Not(right_equal))
        implies_ = Implies(or_, false_)
        equivalence_ = Equivalence(implies_, false_)
        forall_ = ForAll(x, equivalence_)

        expanded_true = Equal(DUMMY_TERM, DUMMY_TERM)
        expanded_false = Not(Equal(DUMMY_TERM, DUMMY_TERM))
        expanded_or_ = Not(And(Not(expanded_true), Not(Not(right_equal))))
        expanded_implies_ = Not(And(expanded_or_, Not(expanded_false)))

        positive_equivalence = And(expanded_implies_, expanded_false)
        negative_equivalence = And(Not(expanded_implies_), Not(expanded_false))
        expanded_equivalence_ = Not(And(Not(positive_equivalence), Not(negative_equivalence)))

        self.assertEqual(fol.expand_formula(true_), expanded_true)
        self.assertEqual(fol.expand_formula(false_), expanded_false)
        self.assertEqual(fol.expand_formula(or_), expanded_or_)
        self.assertEqual(fol.expand_formula(implies_), expanded_implies_)
        self.assertEqual(fol.expand_formula(equivalence_), expanded_equivalence_)
        self.assertEqual(fol.expand_formula(forall_), Not(Exists(x, Not(expanded_equivalence_))))



class TestFOLToNNF(unittest.TestCase):
    def setUp(self):
        self.Person_pred_sym = PredicateSymbol("Person", 2)
        self.Lives_pred_sym = PredicateSymbol("Lives", 2)
        self.LivesIn_fun_sym = FunctionSymbol("LivesIn", 1)

        self.objects = {"john", "paul", "george", "joseph"}
        self.person_tuples = {("john", 20), ("paul", 21), ("george", 22), ("joseph", 23)}
        self.lives_tuples = {("john", "ny"), ("paul", "london"), ("george", "paris"), ("joseph", "paris")}

        self.livesin_function_dictionary = {
            ("john",): "ny",
            ("paul",): "london",
            ("george",): "paris",
            ("joseph",): "paris"
        }

        self.Person = Relation(self.Person_pred_sym, self.person_tuples)
        self.Lives = Relation(self.Lives_pred_sym, self.lives_tuples)
        self.LivesIn = Function(self.LivesIn_fun_sym, self.livesin_function_dictionary)

        self.I = Interpretation.fromRelationsAndFunctions({self.LivesIn}, {self.Person, self.Lives})
        self.alphabet = self.I.alphabet
        self.fol = FOL(self.alphabet)

    def test_to_nnf_allowed_formulas(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        x = Variable.fromString("x")
        right_equal = Equal(x, john)
        not_ = Not(right_equal)
        and_ = And(right_equal, not_)
        exists_ = Exists(x, right_equal)

        self.assertEqual(fol.to_nnf(right_equal), right_equal)
        self.assertEqual(fol.to_nnf(not_), not_)
        self.assertEqual(fol.to_nnf(and_), and_)
        self.assertEqual(fol.to_nnf(exists_), exists_)

    def test_to_nnf_derived_formulas(self):
        fol = self.fol
        john = ConstantTerm.fromString("john")
        x = Variable.fromString("x")
        right_equal = Equal(x, john)
        true_ = TrueFormula()
        false_ = FalseFormula()
        or_ = Or(true_, Not(right_equal))
        implies_ = Implies(or_, false_)
        equivalence_ = Equivalence(implies_, false_)
        forall_true_ = ForAll(x, true_)
        forall_not_or_ = ForAll(x, Not(or_))
        forall_equivalence_ = ForAll(x, equivalence_)

        to_nnf_true_ = Equal(DUMMY_TERM, DUMMY_TERM)
        to_nnf_false_ = Not(Equal(DUMMY_TERM, DUMMY_TERM))
        to_nnf_or_ = Or(to_nnf_true_, Not(right_equal))
        to_nnf_not_or_ = And(Not(to_nnf_true_), right_equal)
        to_nnf_implies_ = Or(to_nnf_not_or_, to_nnf_false_)

        not_to_nnf_implies_ = And(to_nnf_or_, to_nnf_true_)
        positive_equivalence = And(to_nnf_implies_, to_nnf_false_)
        negative_equivalence = And(not_to_nnf_implies_,to_nnf_true_)
        to_nnf_equivalence_ = Or(positive_equivalence, negative_equivalence)


        self.assertEqual(fol.to_nnf(true_), to_nnf_true_)
        self.assertEqual(fol.to_nnf(false_), to_nnf_false_)
        self.assertEqual(fol.to_nnf(or_), to_nnf_or_)
        self.assertEqual(fol.to_nnf(implies_), to_nnf_implies_)
        self.assertEqual(fol.to_nnf(equivalence_), to_nnf_equivalence_)
        self.assertEqual(fol.to_nnf(forall_true_), ForAll(x, to_nnf_true_))
        self.assertEqual(fol.to_nnf(forall_not_or_), ForAll(x, to_nnf_not_or_))
        self.assertEqual(fol.to_nnf(forall_equivalence_), ForAll(x, to_nnf_equivalence_))

