from typing import Set

from pythogic.misc.Symbol import Symbol


class Alphabet(object):
    def __init__(self, symbols: Set[Symbol]):
        self.symbols = symbols

