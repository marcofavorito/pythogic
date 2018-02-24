from pythogic.ltlf.semantics.FiniteTrace import FiniteTrace
from pythogic.ltlf.syntax.LTLfFormula import LTLfFormula, LTLfAtomicProposition, Not, And, Next, Until, \
    DerivedLTLfFormula


def truth(trace: FiniteTrace, position: int, formula: LTLfFormula):
    assert trace.ltlf._is_formula(formula)
    return _truth(trace, position, formula)


def _truth(trace: FiniteTrace, position: int, formula: LTLfFormula):
    if isinstance(formula, LTLfAtomicProposition):
        return formula in trace.get(position)
    elif isinstance(formula, Not):
        return not _truth(trace, position, formula.f)
    elif isinstance(formula, And):
        return _truth(trace, position, formula.f1) and _truth(trace, position, formula.f2)
    elif isinstance(formula, Next):
        return position < trace.last() and _truth(trace, position + 1, formula.f)
    elif isinstance(formula, Until):
        return any(
            _truth(trace, j, formula.f2)
            and all(
                _truth(trace, k, formula.f1) for k in range(position, j)
            )
            for j in range(position, trace.last()+1)
        )
    elif isinstance(formula, DerivedLTLfFormula):
        return _truth(trace, position, formula._equivalent_formula())
    else:
        raise ValueError("Not valid formula")


