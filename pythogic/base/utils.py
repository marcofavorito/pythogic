import re
from itertools import chain, combinations
from PySimpleAutomata import automata_IO

# https://docs.python.org/3/library/itertools.html#recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(set(iterable))
    combs = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    res = set(frozenset(x) for x in combs)
    return res


def my_str(obj):
    s = str(obj)
    s = re.sub("frozenset\(\)", "{}", s)
    s = re.sub("frozenset\(\{(.*)\}\)", "{\g<1>}", s)
    return s


def print_nfa(nfa:dict, name, path):
    str = my_str
    nfa["alphabet"] = set(map(str, nfa["alphabet"]))
    nfa["states"] = set(map(str, nfa["states"]))
    nfa["initial_states"] = set(map(str, nfa["initial_states"]))
    nfa["accepting_states"] = set(map(str, nfa["accepting_states"]))
    nfa["transitions"] = {(str(v[0]), str(v[1])): [str(v[2])] for v in nfa["transitions"]}
    automata_IO.nfa_to_dot(nfa, name, path)
