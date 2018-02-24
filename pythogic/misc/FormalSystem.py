from abc import ABC, abstractmethod
from typing import Set

from pythogic.misc.Alphabet import Alphabet
from pythogic.misc.Formula import Formula
from pythogic.misc.Symbol import Symbol


class FormalSystem(ABC):
    def __init__(self, alphabet: Alphabet):
        assert len(alphabet.symbols) > 0
        self.alphabet = alphabet

    @abstractmethod
    def _is_formula(self, f:Formula):
        raise NotImplementedError
