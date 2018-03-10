========
Pythogic
========

.. image:: https://img.shields.io/pypi/v/pythogic.svg
        :target: https://pypi.python.org/pypi/pythogic

.. image:: https://img.shields.io/pypi/pyversions/pythogic.svg
        :target: https://pypi.python.org/pypi/pythogic

.. image:: https://img.shields.io/travis/MarcoFavorito/pythogic.svg
        :target: https://travis-ci.org/MarcoFavorito/pythogic

.. image:: https://readthedocs.org/projects/pythogic/badge/?version=latest
        :target: https://pythogic.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/MarcoFavorito/pythogic/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/MarcoFavorito/pythogic?branch=master

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
        :alt: MIT License
        :target: https://opensource.org/licenses/MIT

.. image:: https://codecov.io/gh/MarcoFavorito/pythogic/branch/master/graph/badge.svg
        :alt: Codecov coverage
        :target: https://codecov.io/gh/MarcoFavorito/pythogic/branch/master/graph/badge.svg

.. image:: https://img.shields.io/badge/status-development-orange.svg
        :alt: Status: Development
        :target: https://codecov.io/gh/MarcoFavorito/pythogic/branch/master/graph/badge.svg



Python package for deal with logical formulas and formal systems.


* Free software: MIT license
* Documentation: https://pythogic.readthedocs.io.

Usage
--------

First of all, create symbols and an alphabet

.. code:: python

    from pythogic.base.Alphabet import Alphabet
    from pythogic.base.Symbol import Symbol

    a_sym = Symbol("a")
    b_sym = Symbol("b")
    c_sym = Symbol("c")
    alphabet = Alphabet({a_sym, b_sym, c_sym})
    # you can also write:
    alphabet = Alphabet.fromStrings({"a", "b", "c"})

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

Many thanks to PySimpleAutomata_ for the automata support.
.. _PySimpleAutomata: https://github.com/Oneiroe/PySimpleAutomata
