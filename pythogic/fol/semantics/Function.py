from typing import Tuple, Dict

from pythogic.fol.semantics.Object import Object
from pythogic.fol.syntax.Symbol import FunctionSymbol


class Function(object):
    def __init__(self, name, arity, function_dictionary:Dict[Tuple, object]):
        assert Function._is_function_dictionary_valid(arity, function_dictionary)
        self.name = name
        self.arity = arity
        self.function_dictionary = function_dictionary


    @staticmethod
    def fromFunctionSymbol(fun_sym:FunctionSymbol, function_dictionary:Dict[Tuple[Object], Object]):
        assert Function._is_function_dictionary_valid(fun_sym.arity, function_dictionary)
        return Function(fun_sym.name, fun_sym.arity, function_dictionary)


    @staticmethod
    def _is_function_dictionary_valid(arity, function_dictionary:Dict[Tuple[Object], Object]):
        return all(len(t) == arity for t in function_dictionary)


