from typing import Set, Tuple

from pythogic.base.Symbol import PredicateSymbol


class Relation(object):
    def __init__(self, predicate_symbol: PredicateSymbol, tuples:Set[Tuple]):
        assert all(type(t) == tuple and len(t) == predicate_symbol.arity for t in tuples)
        self.predicate_symbol = predicate_symbol
        self.tuples = tuples

    def __str__(self):
        return str(self.predicate_symbol) + " " + str(self.tuples)

    def __repr__(self):
        return str(self.predicate_symbol)

    def _members(self):
        return (self.predicate_symbol, *self.tuples)

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())

    # @staticmethod
    # def _is_function_dictionary_valid(arity, tuples:Set[Tuple[Object]]):
    #     return all(len(t)==arity for t in tuples)



