import math

from config import CONFIG


class Card:
    def __init__(self, number):
        self.number = number
        self.suit = number % 4
        self.value = math.floor(number/4)
        self.value_to_pp = {12: 2, 11: 'A', 10: 'K', 9: 'Q', 8: 'J'}
        self.pp_value = self.value_to_pp[self.value] if self.value in self.value_to_pp else self.value + 3
        self.suit_to_colour = {0: 'blue', 1: 'green', 2: 'red', 3: 'black'}
        self.pp_suit = self.suit_to_colour[self.suit]
        self.colour = CONFIG[self.pp_suit]

    def __repr__(self):
        return str(self.number)
