class BaseBot:
    def __init__(self):
        self.name = "BaseBot"

    @staticmethod
    def choose_cards(last_cards, hand):
        raise NotImplementedError
