from card_list import CardList

def play(some_cards, hand, cards):
    if any(card.number == 0 for card in hand) and not any(card.number == 0 for card in some_cards):
        return 1
    else:
        if quantity_checker(some_cards, cards) == 0 and CardList(some_cards).is_stronger_than(CardList(cards)):
            return 0
        else:
            return 2


def quantity_checker(my_cards, cards):
    if len(my_cards) == 0 or len(cards) == 0:
        return 0
    elif len(my_cards) > 5:
        return 1
    elif len(my_cards) != len(cards):
        return 2
    else:
        return 0


def count_n_tuples(hand, n):
    values = []
    for card in hand:
        values.append(card.value)
    ls = []
    for card in values:
        if values.count(card) == n and card not in ls:
            ls.append(card)
    return len(ls)


class ComputerAlex:
    @staticmethod
    def choose_cards(last_cards, hand):
        num_hand = len(hand)
        num_played = len(last_cards)
        selected_cards = []
        if num_played == 0:
            selected_cards.append(hand[0])
            return selected_cards
        elif num_played > 3:
            return selected_cards
        else:
            for i in range(0, num_hand - num_played + 1):
                selected_cards = hand[i:i+num_played]
                if play(selected_cards, hand, last_cards) == 0:
                    return selected_cards
                else:
                    selected_cards = []
        return selected_cards