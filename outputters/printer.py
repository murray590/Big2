from outputters.outputter import Outputter


class Printer(Outputter):
    def __init__(self):
        self.height = 0
        self.width = 0
        self.card_height = 0
        self.card_width = 0

    def output(self, message):
        print(message)
        with open('file.txt', 'a') as f:
            print(message, file=f)

    def display_cards(self, cards, left, top):
        self.output(cards)

    def display_player(self, player, cards):
        self.output(f"Player {player.name}, wielding {player.bot.name}, to play from their hand of:")

    def display_message(self, message):
        self.output(message)
