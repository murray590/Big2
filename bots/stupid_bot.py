from core.card_list import CardList
from bots.base_bot import BaseBot


class StupidBot(BaseBot):
    def __init__(self):
        self.name = "StupidBot"

    def choose_cards(self, last_card_list, hand):
        num_hand = len(hand)
        num_played = last_card_list.length
        if num_played == 0:
            return [hand[0]]
        elif num_played > 3:
            pass
        else:
            for i in range(0, num_hand - num_played + 1):
                selected_cards = hand[i : i + num_played]
                if CardList(selected_cards).is_valid_play(hand, last_card_list):
                    return selected_cards
            return []
