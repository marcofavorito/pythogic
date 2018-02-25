from typing import Set

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Symbol import FunctionSymbol, PredicateSymbol


class FOLAlphabet(Alphabet):
    def __init__(self, functions: Set[FunctionSymbol], predicates: Set[PredicateSymbol]):
        super().__init__(functions.union(predicates))
        assert len(self.symbols) == len(functions) + len(predicates)
        self.functions = functions
        self.predicates = predicates
