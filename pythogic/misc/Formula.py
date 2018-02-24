from abc import ABC, abstractmethod



class Formula(ABC):
    @abstractmethod
    def _members(self):
        return NotImplementedError

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())
