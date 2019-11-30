class BaseBot:
    def __init__(self):
        self.name = "BaseBot"

    def choose_cards(self, last_cards, hand):
        raise NotImplementedError
