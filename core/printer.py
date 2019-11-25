class Printer:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.card_height = 0
        self.card_width = 0

    def display_cards(self, cards, left, top):
        print(cards)

    def repaint(self, player, cards):
        print(f"Player {player.name}, wielding {player.bot.name}, to play from their hand of:")

    def message(self, message):
        print(message)
