========
Pythogic
========


.. image:: https://img.shields.io/badge/status-development-orange.svg

.. image:: https://img.shields.io/pypi/v/pythogic.svg
        :target: https://pypi.python.org/pypi/pythogic

.. image:: https://img.shields.io/pypi/pyversions/pythogic.svg
        :target: https://pypi.python.org/pypi/pythogic

.. image:: https://img.shields.io/travis/MarcoFavorito/pythogic.svg
        :target: https://travis-ci.org/MarcoFavorito/pythogic

.. image:: https://readthedocs.org/projects/pythogic/badge/?version=latest
        :target: https://pythogic.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/MarcoFavorito/pythogic/badge.svg?branch=master
        :target: https://coveralls.io/github/MarcoFavorito/pythogic?branch=master

.. image:: https://api.codacy.com/project/badge/Grade/653da2a7dda74a3893d87c2f05aa9abd
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/MarcoFavorito/pythogic?utm_source=github.com&utm_medium=referral&utm_content=MarcoFavorito/pythogic&utm_campaign=badger

.. image:: https://api.codacy.com/project/badge/Coverage/51b6bb66aeff4e27ad9a9a19c421803c
        :target: https://www.codacy.com/app/MarcoFavorito/pythogic?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MarcoFavorito/pythogic&amp;utm_campaign=Badge_Coverage

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: MIT License
    :target: https://opensource.org/licenses/MIT

Python package for deal with logical formulas and formal systems.


* Free software: MIT license
* Documentation: https://pythogic.readthedocs.io.

How to use
--------

First of all, create symbols and an alphabet
.. code:: python

    from pythogic.base.Alphabet import Alphabet
    from pythogic.base.Symbol import Symbol

    a_sym = Symbol("a")
    b_sym = Symbol("b")
    c_sym = Symbol("c")
    alphabet = Alphabet({a_sym, b_sym, c_sym})

Create some formulas:
.. code:: python

    from pythogic.base.Formula import AtomicFormula, TrueFormula, FalseFormula, Not, And, Or

    # Propositions
    a = AtomicFormula(a_sym)
    b = AtomicFormula(b_sym)
    c = AtomicFormula(c_sym)

    # Elementary formulas
    not_a = Not(a)
    not_a_and_b = And(Not(a), b)
    not_a_or_c = Or(not_a, c)
    true = TrueFormula()
    false = FalseFormula()

Using Propositional Calculus:
.. code:: python

    from pythogic.pl.PL import PL
    from pythogic.pl.semantics.PLInterpretation import PLInterpretation

    # A dictionary which assign each symbol to a truth value
    symbol2truth = {
            a_sym: True,
            b_sym: False,
            c_sym: True
        }

    # The propositional interpretation
    I = PLInterpretation(alphabet, symbol2truth)

    # main class which contains useful methods
    PL = PL(alphabet)

    PL.truth(a, I)              # returns true
    PL.truth(b, I)              # returns false
    PL.truth(c, I)              # returns true
    PL.truth(not_a, I)          # returns false
    PL.truth(not_a_and_b, I)    # returns false
    PL.truth(not_a_or_c, I)     # returns true
    PL.truth(true, I)           # returns true
    PL.truth(false, I)          # returns false


Features
--------

- Compose logical formula by common syntax rules;
- Implementation of several semantics (FOL Interpretation, finite trace, etc.);
- Support for several logical formal systems: Propositional Logic, First-order Logic, REf, LTLf, LDLf;


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
