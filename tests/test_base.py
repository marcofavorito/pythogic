#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Formula import And, BinaryOperator, AtomicFormula, TrueFormula
from pythogic.base.Symbol import Symbol


class TestFormula(unittest.TestCase):
    def setUp(self):
        pass

    def test_chain(self):
        a_sym, b_sym, c_sym = [Symbol(s) for s in ["a", "b", "c"]]
        a, b, c = [AtomicFormula(s) for s in [a_sym,b_sym,c_sym]]
        and_chain = And.chain([a, b, c])
        self.assertEqual(and_chain, And(a, And(b, And(c, TrueFormula()))))

