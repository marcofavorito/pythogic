from typing import Dict

from pythogic.fol.semantics.Interpretation import Interpretation
from pythogic.fol.syntax.Term import Variable, Term, FunctionTerm


class Assignment(object):

    def __init__(self, variable2object:Dict[Variable,object], interpretation:Interpretation):
        self.variable2object = variable2object
        self.interpretation = interpretation


    def __call__(self, term:Term):
        if isinstance(term, Variable):
            return self.variable2object[term]
        elif isinstance(term, FunctionTerm):
            return self.interpretation.getFunction(term.symbol)(tuple([self(arg) for arg in term.args]))
        else:
            raise ValueError("Term is nor a Variable neither a FunctionTerm")
