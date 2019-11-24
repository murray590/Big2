import random

from core.card import Card


class Dealer:
    def __init__(self, list_of_players):
        self.players = list_of_players
        self.number_of_hands = 4 if len(self.players) == 2 else len(self.players)
        self.deck = [Card(i) for i in range(0, 52)]

    def deal(self):
        random.shuffle(self.deck)
        for index in range(0, len(self.players)):
            self.players[index].hand = self.deck[
                int(index * 52 / self.number_of_hands) : int(
                    (index + 1) * 52 / self.number_of_hands
                )
            ]
            self.players[index].hand.sort(key=lambda card: card.number)

    def who_starts(self):
        lowest_card_numbers = [player.hand[0].number for player in self.players]
        min_card = min(lowest_card_numbers)
        for player in self.players:
            if player.hand[0].number == min_card:
                return player
