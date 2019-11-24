from core.hand import Hand
# from card import Card


class CardList:
    def __init__(self, list_of_cards):
        list_of_cards.sort(key=lambda card: card.number)
        self.cards = list_of_cards
        self.length = len(self.cards)
        self.type = self.type_determiner()
        if self.cards:
            self.kicker = self.cards[2] if self.type in {Hand.FULL_HOUSE, Hand.QUADS} else self.cards[-1]

    def is_valid_quantity(self, cards):
        if self.length == 0 or cards.length == 0:
            return True
        elif self.length > 5:
            print('You must select at most 5 cards!')
            return False
        elif self.length != cards.length:
            print('You must select the same number of cards as the previous play!')
        return True

    def is_stronger_than(self, cards):
        if self.type == cards.type:
            if self.type == Hand.FLUSH:
                if self.kicker.suit.value == cards.kicker.suit.value:
                    return self.kicker.value > cards.kicker.value
                return self.kicker.suit.value > cards.kicker.suit.value
            return self.kicker.number > cards.kicker.number
        return self.type.value > cards.type.value

    def type_determiner(self):
        if self.length == 0:
            return Hand.PASS
        elif self.length == 1:
            return Hand.SINGLE
        elif self.length == 2:
            if self.cards[0].value != self.cards[1].value:
                return Hand.INVALID, "A two card play must be a pair!"
            return Hand.PAIR
        elif self.length == 3:
            if not (self.cards[0].value == self.cards[1].value == self.cards[2].value):
                return Hand.INVALID, "A three card play must be a three of a kind!"
            return Hand.TRIPLE
        elif self.length == 4:
            return Hand.INVALID, "There is no valid four card play, a four of a kind must be played with a kicker!"
        elif self.length == 5:
            return self.five_card_evaluator()
        return Hand.INVALID, "A play must have at most 5 cards!"

    def five_card_evaluator(self):
        if self.length != 5:
            return Hand.INVALID
        v = self.get_relative_values()
        s = self.get_suits()
        if v == [0, 1, 2, 3, 4]:
            if s[0] == s[1] == s[2] == s[3] == s[4]:
                return Hand.STRAIGHT_FLUSH
            else:
                return Hand.STRAIGHT
        elif s[0] == s[1] == s[2] == s[3] == s[4]:
            return Hand.FLUSH
        elif (v[0] == v[1]) and (v[3] == v[4]) and (v[2] == v[1] or v[2] == v[3]):
            return Hand.FULL_HOUSE
        elif (v[0] == v[1] == v[2] == v[3]) or (v[1] == v[2] == v[3] == v[4]):
            return Hand.QUADS
        else:
            return Hand.INVALID

    def get_relative_values(self):
        values = []
        for card in self.cards:
            values.append(card.value - self.cards[0].value)
        return values

    def get_suits(self):
        suits = []
        for card in self.cards:
            suits.append(card.suit)
        return suits

# hand1 = CardList([Card(0), Card(4), Card(8), Card(12), Card(16)])
# hand2 = CardList([Card(35), Card(39), Card(43), Card(47), Card(51)])
#
# print(hand2.is_stronger_than(hand1))
