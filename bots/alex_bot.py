from core.card_list import CardList
from bots.base_bot import BaseBot
from bots import hand_analyser


class AlexBot(BaseBot):
    def __init__(self):
        self.name = "AlexBot"

    def choose_cards(self, last_card_list, hand):
        num_hand = len(hand)
        num_played = last_card_list.length
        if num_played == 0:
            return [hand[0]]
        elif num_played > 3:
            flushes = hand.return_flushes(hand)
            return flushes[0][0:5] if flushes else []
        else:
            for i in range(0, num_hand - num_played + 1):
                selected_cards = hand[i: i + num_played]
                if CardList(selected_cards).is_valid_play(hand, last_card_list):
                    return selected_cards
            return []
