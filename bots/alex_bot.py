from core.card_list import CardList
from bots.base_bot import BaseBot


class AlexBot(BaseBot):
    def __init__(self):
        self.name = "AlexBot"

    @staticmethod
    def choose_cards(last_card_list, hand):
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

    @staticmethod
    def is_there_a_flush(hand):
        suits = [card.suit for card in hand]
        suit_counts = [suits.count(i) for i in range(0, 4)]
        print(suit_counts)
        return any(count >= 5 for count in suit_counts)

    @staticmethod
    def count_n_tuples(hand, n):
        values = [card.value for card in hand]
        ls = {value for value in values if values.count(value) == n}
        return len(ls)
