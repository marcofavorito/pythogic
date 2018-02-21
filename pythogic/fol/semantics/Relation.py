from typing import Set, Tuple

from pythogic.fol.semantics.Object import Object
from pythogic.fol.syntax.Symbol import PredicateSymbol


class Relation(object):
    def __init__(self, name, arity, tuples:Set[Tuple]):
        self.name = name
        self.arity = arity
        self.tuples = tuples

    @staticmethod
    def fromFunctionSymbol(predicate_symbol: PredicateSymbol, tuples:Set[Tuple[Object]]):
        assert Relation._is_function_dictionary_valid(predicate_symbol, tuples)
        return Relation(predicate_symbol.name, predicate_symbol.arity, tuples)

    @staticmethod
    def _is_function_dictionary_valid(arity, tuples:Set[Tuple[Object]]):
        return all(len(t)==arity for t in tuples)



