from abc import ABC, abstractmethod

from pythogic.base.Symbol import PredicateSymbol, Symbol, TrueSymbol, FalseSymbol, LastSymbol, DUMMY_SYMBOL
from pythogic.fol.syntax.Term import Term, Variable

class Expression(ABC):
    @abstractmethod
    def _members(self):
        raise NotImplementedError
    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())


class Formula(Expression):

    def equivalent_formula(self):
        raise NotImplementedError

    def containsVariable(self, v: Variable):
        raise NotImplementedError


class PathExpression(Expression):
    @abstractmethod
    def _members(self):
        raise NotImplementedError

    def __eq__(self, other):
        if type(other) is type(self):
            return self._members() == other._members()
        else:
            return False

    def __hash__(self):
        return hash(self._members())


class AtomicFormula(Formula):

    def __init__(self, symbol:Symbol):
        self.symbol = symbol

    def _members(self):
        return (self.symbol)

    def __str__(self):
        return str(self.symbol)

    def __lt__(self, other):
        return self.symbol.name.__lt__(other.symbol.name)

DUMMY_ATOMIC = AtomicFormula(DUMMY_SYMBOL)

class PredicateFormula(Formula):
    def __init__(self, predicate_symbol: PredicateSymbol, *args: Term):
        assert len(args) == predicate_symbol.arity
        self.predicate_symbol = predicate_symbol
        self.args = args

    def __str__(self):
        return str(self.predicate_symbol) + "(" + ", ".join([t.__str__() for t in self.args]) + ")"


    def _members(self):
        return (self.predicate_symbol, *self.args)

    @classmethod
    def fromString(cls, name: str, *args: Term):
        return PredicateFormula(PredicateSymbol(name, len(args)), *args)

    def containsVariable(self, v:Variable):
        return v in self.args


class Operator(Formula):
    @property
    def operator_symbol(self):
        raise NotImplementedError


class UnaryOperator(Operator):
    def __init__(self, f: Formula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + "(" + str(self.f) + ")"

    def _members(self):
        return (self.operator_symbol, self.f)

    def containsVariable(self, v:Variable):
        return self.f.containsVariable(v)


class BinaryOperator(Operator):
    """A generic binary formula"""

    def __init__(self, f1:Formula, f2:Formula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return str(self.f1) + " " + self.operator_symbol + " " + str(self.f2)

    def containsVariable(self, v:Variable):
        return self.f1.containsVariable(v) or self.f2.containsVariable(v)

    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)


class QuantifiedFormula(Operator):
    def __init__(self, v: Variable, f: Formula):
        self.v = v
        self.f = f

    def containsVariable(self, v: Variable):
        return self.f.containsVariable(v)

    def _members(self):
        return (self.operator_symbol, self.v, self.f)

    def __str__(self):
        return self.operator_symbol + str(self.v) + ".(%s)" % str(self.f)


class Equal(Operator):
    """Equality operator: term_1 = term_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Equal(a, b)
        >>> str(e)
        'a = b'
    """
    operator_symbol = "="
    def __init__(self, t1: Term, t2: Term):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return str(self.t1) + " = " + str(self.t2)

    def containsVariable(self, v:Variable):
        return self.t1 == v or self.t2 == v

    def _members(self):
        return (self.t1, self.operator_symbol, self.t2)


class Not(UnaryOperator):
    """Negation operator: ~formula

    >>> a=Variable.fromString("a")
    >>> A=PredicateFormula.fromString("A", a)
    >>> e = Not(A)
    >>> str(e)
    '~(A^1(a))'

    """
    operator_symbol = "~"


class And(BinaryOperator):
    """And operator: formula_1 & formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> A=PredicateFormula.fromString("A", a); B=PredicateFormula.fromString("B", b)
        >>> e = And(a, b)
        >>> str(e)
        'a & b'
    """
    operator_symbol = "&"


class Or(BinaryOperator):
    """Or operator: formula_1 | formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Or(a, b)
        >>> str(e)
        'a | b'
    """
    operator_symbol = "|"

    def equivalent_formula(self):
        return Not(And(Not(self.f1), Not(self.f2)))


class Implies(BinaryOperator):
    """Logical implication: formula_1 >> formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Implies(a, b)
        >>> str(e)
        'a >> b'
    """
    operator_symbol = ">>"
    def equivalent_formula(self):
        return Or(Not(self.f1), self.f2)


class Exists(QuantifiedFormula):
    operator_symbol = "∃"


class ForAll(QuantifiedFormula):
    operator_symbol = "Ɐ"
    def equivalent_formula(self):
        return Not(Exists(self.v, Not(self.f)))

class Next(UnaryOperator):
    """Next operator: ○(formula_1) """
    operator_symbol = "○"


class Until(BinaryOperator):
    """Until operator: U(formula_1) """
    operator_symbol = "U"


class Eventually(UnaryOperator):
    """Eventually operator: ◇(formula_1) """
    operator_symbol = "◇"

    def equivalent_formula(self):
        return Until(TrueFormula(), self.f)


class Always(UnaryOperator):
    """Always operator: □(formula_1) """
    operator_symbol = "□"
    def equivalent_formula(self):
        return Not(Eventually(Not(self.f)))


class FalseFormula(Formula):
    def _members(self):
        return (FalseSymbol())

    def __str__(self):
        return str(FalseSymbol())

    def equivalent_formula(self):
        return And(Not(DUMMY_ATOMIC), DUMMY_ATOMIC)


class TrueFormula(Formula):
    def _members(self):
        return (TrueSymbol())

    def __str__(self):
        return str(TrueSymbol())

    def equivalent_formula(self):
        return Not(FalseFormula())



class LTLfLast(Formula):
    def _members(self):
        return (LastSymbol())

    def __str__(self):
        return str(LastSymbol())

class PathExpressionFormula(Operator):
    def __init__(self, p: PathExpression, f: Formula):
        self.p = p
        self.f = f

    @property
    def brackets(self):
        raise NotImplementedError


    def _members(self):
        return (self.p, self.brackets, self.f)

    def __str__(self):
        return self.brackets[0] + str(self.p) + self.brackets[1] + "(%s)"%str(self.f)


class PathExpressionUnion(PathExpression):
    operator_symbol = "+"
    def __init__(self, p1:PathExpression, p2:PathExpression):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return str(self.p1) + " " + self.operator_symbol + " " + str(self.p2)

    def _members(self):
        return (self.p1, self.operator_symbol, self.p2)


class PathExpressionSequence(PathExpression):
    operator_symbol = ";"

    def __init__(self, p1:PathExpression, p2:PathExpression):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return str(self.p1) + " " + self.operator_symbol + " " + str(self.p2)

    def _members(self):
        return (self.p1, self.operator_symbol, self.p2)


class PathExpressionStar(PathExpression):
    operator_symbol = "*"

    def __init__(self, p: PathExpression):
        self.p = p

    def __str__(self):
        return "(%s)" % str(self.p) + " " + self.operator_symbol

    def _members(self):
        return (self.p, self.operator_symbol)


class PathExpressionTest(PathExpression):
    operator_symbol = "?"

    def __init__(self, f: Formula):
        self.f = f

    def __str__(self):
        return "(" + str(self.f) + ") " + self.operator_symbol

    def _members(self):
        return (self.f, self.operator_symbol)


class PathExpressionEventually(PathExpressionFormula):
    brackets = "❬❭"


class PathExpressionAlways(PathExpressionFormula):
    brackets = "［］"

    def equivalent_formula(self):
        return Not(PathExpressionEventually(self.p, Not(self.f)))

