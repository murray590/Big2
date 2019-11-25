class Outputter:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.card_width = self.width / 16
        self.card_height = self.height / 8

    def display_player(self, player, cards):
        raise NotImplementedError("This function should display the players name and the previously played cards.")

    def display_cards(self, cards, left, top):
        raise NotImplementedError("This function should display the cards at the location: left, top.")

    def display_message(self, message):
        raise NotImplementedError("This function should display a message.")
