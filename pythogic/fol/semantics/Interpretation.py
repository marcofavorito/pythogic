# -*- coding: utf-8 -*-

"""Implementation of a FOL Interpretation
"""
from typing import Set

from pythogic.fol.semantics import Object
from pythogic.fol.semantics.Function import Function
from pythogic.fol.semantics.Relation import Relation


class Interpretation(object):
    def __init__(self,
                 domain: Set[object],
                 relations: Set[Relation],
                 functions:Set[Function]):
        self.domain = domain
        self.relations = relations
        self.functions = functions

        self._name2relation = {r.name: r for r in relations}
        self._name2function = {f.name: f for f in functions}

    @staticmethod
    def fromRelationsAndFunctions(relations: Set[Relation], functions:Set[Function]):
        domain = set(e for r in relations for t in r.tuples for e in t).union(set([*x] + [*y] for f in functions for x, y in f.function_dictionary))
        constants = set(Function(
            str(o),
            0,
            {():o}
        ) for o in domain)
        return Interpretation(domain, relations, functions.union(constants))

    def getRelation(self, name):
        return self._name2relation[name]

    def getFunction(self, name):
        return self._name2function[name]

