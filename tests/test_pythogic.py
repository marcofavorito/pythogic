#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pythogic` package."""

import unittest

from pythogic.base.Symbol import Symbol
from pythogic.base.utils import powerset


class TestPythogic(unittest.TestCase):
    """Tests for `pythogic` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_powerset(self):
        a = Symbol("a")
        b = Symbol("b")
        c = Symbol("c")
        d = Symbol("d")
        s = [a,b,c,d]
        ps = powerset(s)
        true_ps = {
            (),
            (a,),(b,),(c,),(d,),
            (a, b), (a, c), (a, d), (b, c), (b, d), (c, d),
            (a,b,c), (a,b,d), (a,c,d), (b,c,d),
            (a, b, c, d)

        }
        self.assertTrue(ps == true_ps)
