from abc import ABC, abstractmethod
from typing import Set, Dict, Callable, Type

from pythogic.base.Alphabet import Alphabet
from pythogic.base.Formula import Formula, And


class FormalSystem(ABC):
    def __init__(self, alphabet: Alphabet):
        self.alphabet = alphabet

    @property
    @abstractmethod
    def allowed_formulas(self) -> Set[Formula]:
        """Set of elementary formulas which generate all the possible formulas of the formal language."""
        raise NotImplementedError

    @property
    @abstractmethod
    def derived_formulas(self) -> Dict[Formula, Callable[[Type[Formula]], Callable[[Formula], Formula]]]:
        """Set of formulas syntactically allowed in the formal system
        but rewritable with elementary formula expressions (i.e. allowed formulas)."""
        raise NotImplementedError

    @abstractmethod
    def _is_formula(self, f:Formula):
        """Check if a formula is syntactically legal in the current formal system"""
        raise NotImplementedError

    @abstractmethod
    def _truth(self, f:Formula, *args):
        """Private method for evaluate the truth of the formula.
        Has to be implemented in every subclass of FormalSystem.
        No further specifications of other arguments,
        but should contain semantics for formulas evaluation.
        """
        raise NotImplementedError

    @abstractmethod
    def _expand_formula(self, f:Formula):
        """Private method for rewrite formulas (both allowed and derived ones)
        by using only elementary formulas."""
        raise NotImplementedError

    @abstractmethod
    def to_nnf(self, f:Formula):
        """Normalize the formula into Negative Normal Form (i.e.
        Not formula only in front of Atomic Formulas)."""
        raise NotImplementedError

    def to_equivalent_formula(self, derived_formula:Formula):
        """Given a derived formula, return the equivalent formula
        rewritten with elementary formula expressions (i.e. allowed formula)."""
        return self.derived_formulas[type(derived_formula)](derived_formula)


    def expand_formula(self, f:Formula):
        """Formula expansion. It calls `_expand_formula`.
        See `_expand_formula` other for details.
        """
        if type(f) in self.derived_formulas:
            return self.expand_formula(self.to_equivalent_formula(f))
        else:
            return self._expand_formula(f)

    def truth(self, f:Formula, *args) -> bool:
        """Formula evaluation.
        It calls `_truth` with all the provided arguments.
        :param Formula f: the formula to evaluate.
        :param *args: arguments to provide semantics to the formal system. Has to be defined properly by subclasses.
        :return bool, the formula truth.
        :raises ValueError: if the formula is not vaild in the current Formal System"
        """
        expanded_formula = self.expand_formula(f)
        if not self.is_formula(expanded_formula):
            raise ValueError("Formula is not vaild in the current Formal System")
        # if type(f) in self.derived_formulas:
        #     return self.truth(self.to_equivalent_formula(f), *args)
        # else:
        #     return self._truth(f, *args)
        return self._truth(expanded_formula, *args)

    def is_formula(self, f: Formula):
        """Syntactic check on the formula.
        It calls `_is_formula`.
        """
        if type(f) in self.derived_formulas:
            return self.is_formula(self.to_equivalent_formula(f))
        elif type(f) in self.allowed_formulas:
            return self._is_formula(f)
        else:
            return False
