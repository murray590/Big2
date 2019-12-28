from core.hand_type import HandType


class CardList:
    def __init__(self, list_of_cards):
        if list_of_cards:
            list_of_cards.sort(key=lambda card: card.number)
        self.cards = list_of_cards
        self.length = len(self.cards)
        self.type = self.type_determiner()
        if self.cards:
            self.kicker = (
                self.cards[2]
                if self.type in {HandType.FULL_HOUSE, HandType.QUADS}
                else self.cards[-1]
            )

    def is_valid_play(self, hand, cards):
        if any(card.number == 0 for card in hand) and not any(
            card.number == 0 for card in self.cards
        ):
            return "You must include the blue 3 in your play"
        elif self.type == HandType.PASS:
            return True
        return self.is_valid_quantity(cards) and self.is_stronger_than(cards)

    def is_valid_quantity(self, cards):
        if self.length == 0 or cards.length == 0:
            return True
        elif self.length > 5:
            print("You must select at most 5 cards!")
            return False
        elif self.length != cards.length:
            print("You must select the same number of cards as the previous play!")
        return True

    def is_stronger_than(self, cards):
        if self.type == cards.type:
            if self.type == HandType.FLUSH:
                if self.kicker.suit.value == cards.kicker.suit.value:
                    return self.kicker.value > cards.kicker.value
                return self.kicker.suit.value > cards.kicker.suit.value
            return self.kicker.number > cards.kicker.number
        return self.type.value > cards.type.value

    def type_determiner(self):
        if self.length == 0:
            return HandType.PASS
        elif self.length == 1:
            return HandType.SINGLE
        elif self.length == 2:
            if self.cards[0].value != self.cards[1].value:
                return HandType.INVALID, "A two card play must be a pair!"
            return HandType.PAIR
        elif self.length == 3:
            if not (self.cards[0].value == self.cards[1].value == self.cards[2].value):
                return HandType.INVALID, "A three card play must be a three of a kind!"
            return HandType.TRIPLE
        elif self.length == 4:
            return (
                HandType.INVALID,
                "There is no valid four card play, a four of a kind must be played with a kicker!",
            )
        elif self.length == 5:
            return self.five_card_evaluator()
        return HandType.INVALID, "A play must have at most 5 cards!"

    def five_card_evaluator(self):
        if self.length != 5:
            return HandType.INVALID
        v = self.get_relative_values()
        s = self.get_suits()
        if v == [0, 1, 2, 3, 4]:
            if s[0] == s[1] == s[2] == s[3] == s[4]:
                return HandType.STRAIGHT_FLUSH
            else:
                return HandType.STRAIGHT
        elif s[0] == s[1] == s[2] == s[3] == s[4]:
            return HandType.FLUSH
        elif (v[0] == v[1]) and (v[3] == v[4]) and (v[2] == v[1] or v[2] == v[3]):
            return HandType.FULL_HOUSE
        elif (v[0] == v[1] == v[2] == v[3]) or (v[1] == v[2] == v[3] == v[4]):
            return HandType.QUADS
        else:
            return HandType.INVALID

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
