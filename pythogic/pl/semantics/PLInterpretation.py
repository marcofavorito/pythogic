from typing import Dict

from pythogic.misc.Alphabet import Alphabet
from pythogic.misc.Symbol import Symbol
from pythogic.pl.syntax.PLFormula import PLFormula, AtomicFormula, Not, And, Or


class PLInterpretation(object):
    def __init__(self, alphabet: Alphabet, symbol2truth:Dict[Symbol, bool]):
        assert alphabet.symbols == symbol2truth.keys() and all(type(v)==bool for v in symbol2truth.values())
        self.alphabet = alphabet
        self.symbol2truth = symbol2truth

    def __call__(self, f:PLFormula):
        if isinstance(f, AtomicFormula):
            assert f.symbol in self.alphabet
            return self.symbol2truth[f.symbol]
        elif isinstance(f, Not):
            return not self(f.f)
        elif isinstance(f, And):
            return self(f.f1) and self(f.f2)
        elif isinstance(f, Or):
            return self(f.f1) and self(f.f2)
        else:
            raise ValueError("Term is nor a Variable neither a FunctionTerm")
