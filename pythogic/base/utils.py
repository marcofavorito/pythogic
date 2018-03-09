import re
from itertools import chain, combinations
from PySimpleAutomata import automata_IO

# https://docs.python.org/3/library/itertools.html#recipes
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(set(iterable))
    combs = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    res = set(frozenset(x) for x in combs)
    # res = map(frozenset, combs)
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

    # more destinations for the same start state and action
    import collections
    transitions = collections.defaultdict(list)
    for v in nfa["transitions"]:
        transitions[(str(v[0]), str(v[1]))].append(str(v[2]))

    nfa["transitions"] = transitions
    automata_IO.nfa_to_dot(nfa, name, path)
