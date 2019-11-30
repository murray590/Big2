def is_there_a_flush(hand):
    suits = [card.suit for card in hand]
    suit_counts = [suits.count(i) for i in range(0, 4)]
    return any(count >= 5 for count in suit_counts)


def return_flushes(hand):
    suits = [[card for card in hand if card.suit == suit] for suit in range(0, 4)]
    flushes = [cards for cards in suits if len(cards) >= 5]
    return flushes


def count_n_tuples(hand, n):
    values = [card.value for card in hand]
    ls = {value for value in values if values.count(value) == n}
    return len(ls)
