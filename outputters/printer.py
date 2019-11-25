from outputters.outputter import Outputter


class Printer(Outputter):
    def __init__(self):
        self.height = 0
        self.width = 0
        self.card_height = 0
        self.card_width = 0

    def display_cards(self, cards, left, top):
        print(cards)

    def display_player(self, player, cards):
        print(f"Player {player.name}, wielding {player.bot.name}, to play from their hand of:")

    def display_message(self, message):
        print(message)
