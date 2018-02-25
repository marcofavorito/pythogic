# -*- coding: utf-8 -*-

"""Implementation of a FOL Interpretation
"""
from functools import reduce
from typing import Set

from pythogic.fol.semantics.Function import Function
from pythogic.fol.semantics.Relation import Relation
from pythogic.fol.syntax.FOLAlphabet import FOLAlphabet
from pythogic.base.Symbol import FunctionSymbol, PredicateSymbol, ConstantSymbol


class Interpretation(object):
    def __init__(self,
                 alphabet: FOLAlphabet,
                 domain: Set[object],
                 relations: Set[Relation],
                 functions:Set[Function]):
        self.alphabet = alphabet
        self.domain = domain
        self.relations = relations
        self.functions = functions

        self._symbol2relation = {r.predicate_symbol: r for r in relations}
        self._symbol2function = {f.function_symbol:  f for f in functions}


    @staticmethod
    def fromRelationsAndFunctions(functions:Set[Function], relations: Set[Relation]):
        function_symbols  = set(f.function_symbol  for f in functions)
        predicate_symbols = set(r.predicate_symbol for r in relations)

        objects_from_relations = set(e for r in relations for t in r.tuples for e in t)
        objects_from_functions = set(reduce(lambda x,y: x.union(y), [set(x).union({y}) for f in functions for x, y in f.function_dictionary.items()], set()))
        domain = objects_from_relations.union(objects_from_functions)
        constants = set(Function(
            ConstantSymbol(str(o)),
            {():o}
        ) for o in domain)
        constants_symbols = set(ConstantSymbol(str(o)) for o in domain)

        alphabet = FOLAlphabet(function_symbols.union(constants_symbols), predicate_symbols)
        return Interpretation(alphabet, domain, relations, functions.union(constants))

    def getRelation(self, name: PredicateSymbol):
        assert name in self._symbol2relation
        return self._symbol2relation[name]

    def getFunction(self, name: FunctionSymbol):
        assert name in self._symbol2function
        return self._symbol2function[name]

    def isValidFunction(self, function:Function):
        return all(all(e in self.domain for e in x) and y in self.domain for x,y in function.function_dictionary)

    def isValidRelation(self, relation:Relation):
        return all(e in self.domain for t in relation.tuples for e in t)



