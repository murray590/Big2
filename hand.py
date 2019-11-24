from enum import Enum


class Hand(Enum):
    INVALID = 1
    PASS = 2
    SINGLE = 3
    PAIR = 4
    TRIPLE = 5
    STRAIGHT = 6
    FLUSH = 7
    FULL_HOUSE = 8
    QUADS = 9
    STRAIGHT_FLUSH = 10
