from typing import Dict

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import Symbol
from pythogic.base.Formula import AtomicFormula, Formula


class PLInterpretation(object):
    def __init__(self, alphabet: Alphabet, symbol2truth:Dict[Symbol, bool]):
        assert alphabet.symbols == symbol2truth.keys() and all(type(v)==bool for v in symbol2truth.values())
        self.alphabet = alphabet
        self.symbol2truth = symbol2truth


    def __eq__(self, other):
        if type(self) == type(other):
            return self.alphabet == other.alphabet and self.symbol2truth == other.symbol2truth
        else:
            return False

    def _members(self):
        return self.alphabet, tuple(sorted(self.symbol2truth.items()))

    def __hash__(self):
        return hash(self._members())
