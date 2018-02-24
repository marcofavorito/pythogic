from typing import List, Set

from pythogic.ltlf.syntax.LTLf import LTLf
from pythogic.ltlf.syntax.LTLfFormula import LTLfAtomicProposition


class FiniteTrace(object):
    def __init__(self, trace: List[Set[LTLfAtomicProposition]], ltlf: LTLf):
        assert FiniteTrace._is_valid_trace(trace, ltlf)
        self.trace = trace
        self.ltlf = ltlf

    def length(self):
        return len(self.trace)

    def last(self):
        return len(self.trace)-1

    def _position_is_legal(self, position:int):
        return position>=0 and position <= self.last()

    def get(self, position:int) -> Set[LTLfAtomicProposition]:
        assert self._position_is_legal(position)
        return self.trace[position]

    def segment(self, start:int, end:int) :
        assert self._position_is_legal(start)
        assert self._position_is_legal(end)
        return FiniteTrace(self.trace[start: end+1])

    @staticmethod
    def _is_valid_trace(trace :List[Set[LTLfAtomicProposition]], ltlf: LTLf):
        return all(all(e in ltlf.propositions for e in t) for t in trace)


    def __str__(self):
        return "Trace (length=%s)" %self.length() + "\n\t" + \
            "\n\t".join("%d: {"%i + ", ".join(map(str,sorted(e))) + "}"  for i, e in enumerate(self.trace))
