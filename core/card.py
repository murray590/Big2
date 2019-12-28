import math

from outputters.graphics import Colour


class Card:
    def __init__(self, number):
        self.number = number
        self.suit = number % 4
        self.value = math.floor(number / 4)
        self.colour = self.suit_to_colour()
        self.pp_value = self.value_to_pp()
        self.pp_suit = self.suit_to_pp()

    def __repr__(self):
        return f"{self.pp_value}{self.pp_suit}"

    # def __eq__(self, other):
    #     if not isinstance(other, Card):
    #         return False
    #     return self.number == other.number

    def suit_to_colour(self):
        return {
            0: Colour.BLUE,
            1: Colour.GREEN,
            2: Colour.RED,
            3: Colour.BLACK,
        }[self.suit].value

    def value_to_pp(self):
        pp = {12: 2, 11: "A", 10: "K", 9: "Q", 8: "J"}
        return pp[self.value] if self.value in pp else self.value + 3

    def suit_to_pp(self):
        return {0: "d", 1: "c", 2: "h", 3: "s"}[self.suit]
