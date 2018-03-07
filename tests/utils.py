from PySimpleAutomata import automata_IO
import re

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
