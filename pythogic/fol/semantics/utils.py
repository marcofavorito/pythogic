from pythogic.fol.semantics.Assignment import Assignment
from pythogic.fol.syntax.Formula import Formula, Equal, PredicateFormula, Not, And, Or, Implies, Exists, ForAll


def truth(assignment: Assignment, formula: Formula):
    assert assignment.interpretation.fol._is_formula(formula)

    if isinstance(formula, Equal):
        return assignment(formula.t1) == assignment(formula.t2)
    elif isinstance(formula, PredicateFormula):
        return tuple(assignment(t) for t in formula.args) in assignment.interpretation.getRelation(
            formula.predicate_symbol).tuples
    elif isinstance(formula, Not):
        return not truth(assignment, formula.f)
    elif isinstance(formula, And):
        return truth(assignment, formula.f1) and truth(assignment, formula.f2)
    elif isinstance(formula, Or):
        return truth(assignment, formula.f1) or truth(assignment, formula.f2)
    elif isinstance(formula, Implies):
        return not truth(assignment, formula.f1) or truth(assignment, formula.f2)
    elif isinstance(formula, Exists):
        # assert formula.v not in assignment.variable2object
        res = False
        for el in assignment.interpretation.domain:
            new_mapping = assignment.variable2object.copy()
            new_mapping[formula.v] = el
            res = res or truth(Assignment(new_mapping, assignment.interpretation), formula.f)
            if res: break
        return res
    elif isinstance(formula, ForAll):
        # assert formula.v not in assignment.variable2object
        res = True
        for el in assignment.interpretation.domain:
            new_mapping = assignment.variable2object.copy()
            new_mapping[formula.v] = el
            res = res and truth(Assignment(new_mapping, assignment.interpretation), formula.f)
            if not res: break
        return res
    else:
        raise ValueError("Formula not recognized")
