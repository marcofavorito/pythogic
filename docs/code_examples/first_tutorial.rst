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
