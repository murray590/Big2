from core.card_list import CardList


class Player:
    def __init__(self, name, computer):
        self.hand = []
        self.last_played_cards = CardList([])
        self.name = name
        self.computer = computer

    def opponents(self, people):
        opponents = list(people)
        opponents.remove(self)
        return opponents

    def next_player(self, people):
        return people[(people.index(self) + 1) % len(people)]