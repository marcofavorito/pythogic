from abc import ABC, abstractmethod
from typing import Set, Dict

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Formula import Formula, And


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
    def derived_formulas(self) -> Dict[Formula, Formula]:
        raise NotImplementedError

    @abstractmethod
    def to_equivalent_formula(self, derived_formula:Formula):
        raise NotImplementedError

    @abstractmethod
    def _is_formula(self, f:Formula):
        """Check if a formula is legal in the current formal system"""
        raise NotImplementedError

    @abstractmethod
    def _truth(self, *args):
        raise NotImplementedError

    @abstractmethod
    def _expand_formula(self, f:Formula):
        raise NotImplementedError

    def expand_formula(self, f:Formula):
        if type(f) in self.derived_formulas:
            return self.expand_formula(self.to_equivalent_formula(f))
        else:
            self._expand_formula(f)

    def truth(self, f:Formula, *args):
        assert self.is_formula(f)
        if type(f) in self.derived_formulas:
            return self.truth(self.to_equivalent_formula(f), *args)
        else:
            return self._truth(f, *args)

    def is_formula(self, f: Formula):
        if type(f) in self.derived_formulas:
            return self.is_formula(self.to_equivalent_formula(f))
        else:
            # assert type(f) in self.allowed_formulas
            return self._is_formula(f)
