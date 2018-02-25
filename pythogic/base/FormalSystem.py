from abc import ABC, abstractmethod
from typing import Set

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Formula import Formula


class FormalSystem(ABC):
    def __init__(self, alphabet: Alphabet):
        assert len(alphabet.symbols) > 0
        self.alphabet = alphabet

    @property
    @abstractmethod
    def allowed_formulas(self) -> Set[Formula]:
        raise NotImplementedError

    @property
    @abstractmethod
    def derived_formulas(self) -> Set[Formula]:
        raise NotImplementedError

    @abstractmethod
    def _is_formula(self, f:Formula):
        """Check if a formula is legal in the current formal system"""
        raise NotImplementedError

    @abstractmethod
    def _truth(self, *args):
        raise NotImplementedError

    def truth(self, f:Formula, *args):
        assert self.is_formula(f)
        if type(f) in self.derived_formulas:
            return self.truth(f.equivalent_formula(), *args)
        else:
            return self._truth(f, *args)

    def is_formula(self, f: Formula):
        if type(f) in self.derived_formulas:
            return self.is_formula(f.equivalent_formula())
        else:
            assert type(f) in self.allowed_formulas
            return self._is_formula(f)
