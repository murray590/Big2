class Printer:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.card_height = 0
        self.card_width = 0

    def display_cards(self, cards, left, top):
        print(cards)

    def repaint(self, player, cards):
        print(f"Player {player.name} to play, the last played cards were: {cards}")

    def message(self, message):
        print(message)
