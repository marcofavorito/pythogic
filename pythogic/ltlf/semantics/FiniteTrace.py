from typing import List, Set

from pythogic.base.Formula import AtomicFormula
from pythogic.base.Alphabet import Alphabet


class FiniteTrace(object):
    def __init__(self, trace: List[Set[AtomicFormula]], alphabet: Alphabet):
        assert FiniteTrace._is_valid_trace(trace, alphabet)
        self.trace = trace
        self.alphabet = alphabet

    def length(self):
        return len(self.trace)

    def last(self):
        return len(self.trace)-1

    def _position_is_legal(self, position:int):
        return position>=0 and position <= self.last()

    def get(self, position:int) -> Set[AtomicFormula]:
        assert self._position_is_legal(position)
        return self.trace[position]

    def segment(self, start:int, end:int) :
        assert self._position_is_legal(start)
        assert self._position_is_legal(end)
        return FiniteTrace(self.trace[start: end], self.alphabet)

    @staticmethod
    def _is_valid_trace(trace :List[Set[AtomicFormula]], alphabet: Alphabet):
        return all(all(e.symbol in alphabet.symbols for e in t) for t in trace)


    def __str__(self):
        return "Trace (length=%s)" %self.length() + "\n\t" + \
            "\n\t".join("%d: {"%i + ", ".join(map(str,sorted(e))) + "}"  for i, e in enumerate(self.trace))
