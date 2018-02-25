from typing import Tuple, Dict

from pythogic.base.Symbol import FunctionSymbol


class Function(object):
    def __init__(self, function_symbol: FunctionSymbol, function_dictionary:Dict[Tuple, object]):
        assert all(type(t) == tuple and len(t) == function_symbol.arity for t in function_dictionary)
        self.function_symbol = function_symbol
        self.function_dictionary = function_dictionary

    def __str__(self):
        return str(self.function_symbol) + " " + str(self.function_dictionary)

    def __repr__(self):
        return str(self.function_symbol)

    def _members(self):
        return (self.function_symbol, tuple(sorted(self.function_dictionary.items())))

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())

    def __call__(self, *args):
        assert len(args) == self.function_symbol.arity and args in self.function_dictionary
        return self.function_dictionary[args]

    # @staticmethod
    # def _is_function_dictionary_valid(arity, function_dictionary:Dict[Tuple[Object], Object]):
    #     return all(len(t) == arity for t in function_dictionary)


