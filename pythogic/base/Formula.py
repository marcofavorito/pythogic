from abc import ABC, abstractmethod

from pythogic.base.Symbol import PredicateSymbol, Symbol, TrueSymbol, FalseSymbol, LastSymbol, DUMMY_SYMBOL
from pythogic.base.Symbols import Symbols
from pythogic.fol.syntax.Term import Term, Variable, ConstantTerm


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

    def __repr__(self):
        return self.__str__()


class Formula(Expression):
    pass

class PathExpression(Expression):
    pass


class AtomicFormula(Formula):

    def __init__(self, symbol:Symbol):
        self.symbol = symbol

    def _members(self):
        return (self.symbol)

    def __str__(self):
        return str(self.symbol)

    def __lt__(self, other):
        return self.symbol.name.__lt__(other.symbol.name)

    @classmethod
    def fromName(cls, name:str):
        return cls(Symbol(name))


DUMMY_ATOMIC = AtomicFormula(DUMMY_SYMBOL)
DUMMY_TERM = ConstantTerm.fromString(DUMMY_SYMBOL.name)

class PredicateFormula(Formula):
    def __init__(self, predicate_symbol: PredicateSymbol, *args: Term):
        assert len(args) == predicate_symbol.arity
        self.predicate_symbol = predicate_symbol
        self.args = args

    def __str__(self):
        return str(self.predicate_symbol) + "(" + ", ".join([t.__str__() for t in self.args]) + ")"

    def _members(self):
        sorted_args = sorted(self.args)
        return (self.predicate_symbol, *sorted_args)

    @classmethod
    def fromString(cls, name: str, *args: Term):
        return PredicateFormula(PredicateSymbol(name, len(args)), *args)




class Operator(Formula):
    base_expression = Symbols.ROUND_BRACKET_LEFT.value + "%s" + Symbols.ROUND_BRACKET_RIGHT.value

    @property
    def operator_symbol(self):
        raise NotImplementedError


class UnaryOperator(Operator):
    def __init__(self, f: Formula):
        self.f = f

    def __str__(self):
        return self.operator_symbol + Symbols.ROUND_BRACKET_LEFT.value + str(self.f) + Symbols.ROUND_BRACKET_RIGHT.value

    def _members(self):
        return (self.operator_symbol, self.f)


    def __lt__(self, other):
        return self.f.__lt__(other.f)


class BinaryOperator(Operator):
    """A generic binary formula"""

    def __init__(self, f1:Formula, f2:Formula):
        self.f1 = f1
        self.f2 = f2

    def __str__(self):
        return self.base_expression % (str(self.f1) + " " + self.operator_symbol + " " + str(self.f2))


    def _members(self):
        return (self.f1, self.operator_symbol, self.f2)


class CommutativeBinaryOperator(BinaryOperator):
    """A generic binary formula"""

    def __init__(self, f1:Formula, f2:Formula):
        _f1, _f2 = sorted([f1, f2], key=lambda x: x.__str__())
        super().__init__(_f1,_f2)



class QuantifiedFormula(Operator):
    def __init__(self, v: Variable, f: Formula):
        self.v = v
        self.f = f

    def _members(self):
        return (self.operator_symbol, self.v, self.f)

    def __str__(self):
        return self.operator_symbol + str(self.v) + "."+ self.base_expression % str(self.f)


class Equal(Operator):
    """Equality operator: term_1 = term_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Equal(a, b)
        >>> str(e)
        'a = b'
    """
    operator_symbol = Symbols.EQUAL.value
    def __init__(self, t1: Term, t2: Term):
        self.t1 = t1
        self.t2 = t2

    def __str__(self):
        return str(self.t1) + " " + self.operator_symbol + " " + str(self.t2)

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
    operator_symbol = Symbols.NOT.value


class And(CommutativeBinaryOperator):
    """And operator: formula_1 & formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> A=PredicateFormula.fromString("A", a); B=PredicateFormula.fromString("B", b)
        >>> e = And(a, b)
        >>> str(e)
        '(a & b)'
        >>> e = And(b, a)
        >>> str(e)
        '(a & b)'
    """
    operator_symbol = Symbols.AND.value


class Or(CommutativeBinaryOperator):
    """Or operator: formula_1 | formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Or(a, b)
        >>> str(e)
        '(a | b)'
        >>> e = Or(b, a)
        >>> str(e)
        '(a | b)'
    """
    operator_symbol = Symbols.OR.value


class Implies(BinaryOperator):
    """Logical implication: formula_1 >> formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Implies(a, b)
        >>> str(e)
        '(a >> b)'
    """
    operator_symbol = Symbols.IMPLIES.value

class Equivalence(BinaryOperator):
    """Equivalence: formula_1 === formula_2

        >>> a=Variable.fromString("a"); b=Variable.fromString("b")
        >>> e = Equivalence(a, b)
        >>> str(e)
        '(a === b)'
    """
    operator_symbol = Symbols.EQUIVALENCE.value



class Exists(QuantifiedFormula):
    operator_symbol = Symbols.EXISTS.value


class ForAll(QuantifiedFormula):
    operator_symbol = Symbols.FORALL.value


class Next(UnaryOperator):
    """Next operator: ○(formula_1) """
    operator_symbol = Symbols.NEXT.value


class Until(BinaryOperator):
    """Until operator: U(formula_1) """
    operator_symbol = Symbols.UNTIL.value


class Eventually(UnaryOperator):
    """Eventually operator: ◇(formula_1) """
    operator_symbol = Symbols.EVENTUALLY.value


class Always(UnaryOperator):
    """Always operator: □(formula_1) """
    operator_symbol = Symbols.ALWAYS.value



class FalseFormula(Formula):
    def _members(self):
        return (FalseSymbol())

    def __str__(self):
        return str(FalseSymbol())




class TrueFormula(Formula):
    def _members(self):
        return (TrueSymbol())

    def __str__(self):
        return str(TrueSymbol())

class LDLfLast(Formula):
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
        return self.brackets[0] + str(self.p) + self.brackets[1] + self.base_expression % str(self.f)


class PathExpressionUnion(PathExpression):
    operator_symbol = Symbols.PATH_UNION.value
    def __init__(self, p1:PathExpression, p2:PathExpression):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return str(self.p1) + " " + self.operator_symbol + " " + str(self.p2)

    def _members(self):
        return (self.p1, self.operator_symbol, self.p2)


class PathExpressionSequence(PathExpression):
    operator_symbol = Symbols.PATH_SEQUENCE.value

    def __init__(self, p1:PathExpression, p2:PathExpression):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return str(self.p1) + " " + self.operator_symbol + " " + str(self.p2)

    def _members(self):
        return (self.p1, self.operator_symbol, self.p2)


class PathExpressionStar(PathExpression):
    operator_symbol = Symbols.PATH_STAR.value

    def __init__(self, p: PathExpression):
        self.p = p

    def __str__(self):
        return "(%s)" % str(self.p) + " " + self.operator_symbol

    def _members(self):
        return (self.p, self.operator_symbol)


class PathExpressionTest(PathExpression):
    operator_symbol = Symbols.PATH_TEST.value

    def __init__(self, f: Formula):
        self.f = f

    def __str__(self):
        return "(" + str(self.f) + ") " + self.operator_symbol

    def _members(self):
        return (self.f, self.operator_symbol)


class PathExpressionEventually(PathExpressionFormula):
    brackets = Symbols.ANGLE_BRACKET_LEFT.value + Symbols.ANGLE_BRACKET_RIGHT.value


class PathExpressionAlways(PathExpressionFormula):
    brackets = Symbols.FULLWIDTH_SQUARE_BRACKET_LEFT.value + Symbols.FULLWIDTH_SQUARE_BRACKET_RIGHT.value


class LogicalTrue(Formula):
    def _members(self):
        return (Symbol(Symbols.LOGICAL_TRUE.value))

    def __str__(self):
        return str(Symbol(Symbols.LOGICAL_TRUE.value))

class LogicalFalse(Formula):
    def _members(self):
        return (Symbol(Symbols.LOGICAL_FALSE.value))

    def __str__(self):
        return str(Symbol(Symbols.LOGICAL_FALSE.value))

class End(Formula):
    def _members(self):
        return (Symbol(Symbols.END.value))

    def __str__(self):
        return str(Symbol(Symbols.END.value))
