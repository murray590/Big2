import math

from core.graphics import Colour


class Card:
    def __init__(self, number):
        self.number = number
        self.suit = number % 4
        self.value = math.floor(number/4)
        self.suit_to_colour = {0: Colour.BLUE, 1: Colour.GREEN, 2: Colour.RED, 3: Colour.BLACK}
        self.colour = self.suit_to_colour[self.suit].value
        self.value_to_pp = {12: 2, 11: 'A', 10: 'K', 9: 'Q', 8: 'J'}
        self.pp_value = self.value_to_pp[self.value] if self.value in self.value_to_pp else self.value + 3
        self.pp_suit = {0: 'd', 1: 'c', 2: 'h', 3: 's'}[self.suit]

    def __repr__(self):
        return f"{self.pp_value}{self.pp_suit}"
