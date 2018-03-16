from typing import Tuple, Dict

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Formula import Formula
from pythogic.pl.PL import PL
from pythogic.pl.semantics.PLInterpretation import PLInterpretation


class Sink(object):
    def __str__(self):
        return "sink"

    def __eq__(self, other):
        return type(self)==type(other)

    def __hash__(self):
        return hash(type(self))




