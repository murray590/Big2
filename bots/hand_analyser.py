from core.hand_type import HandType
from core.card_list import CardList


class HandAnalyser:
    def __init__(self, cards):
        cards.sort(key=lambda card: card.number)
        self.cards = cards

    def find_possible_plays(self, last_played_cl):
        if last_played_cl.type == HandType.INVALID:
            return "Previous play was invalid."
        elif last_played_cl.length == 0:
            possible_plays = self.find_5_card_plays()
            for i in {1, 2, 3}:
                possible_plays += self.find_n_tuples(i)
        elif last_played_cl.length in {1, 2, 3}:
            possible_plays = self.find_n_tuples(last_played_cl.length)
        elif last_played_cl.length == 5:
            possible_plays = self.find_5_card_plays()
        else:
            return "Invalid play."
        return self.filter_valid(possible_plays, last_played_cl)

    def find_5_card_plays(self):
        return self.find_straights() + self.find_flushes() + self.find_full_houses() + self.find_quads() + self.find_straight_flushes()

    def is_there_a_flush(self):
        suits = [card.suit for card in self.cards]
        suit_counts = [suits.count(i) for i in range(0, 4)]
        return any(count >= 5 for count in suit_counts)

    def find_flushes(self):
        suits = [[card for card in self.cards if card.suit == suit] for suit in range(0, 4)]
        flushes = [cards[:5] for cards in suits if len(cards) >= 5]
        return flushes
    
    def find_straights(self):
        card_values = []
        unique_cards = []
        for card in self.cards:
            if card.value not in card_values:
                unique_cards.append(card)
                card_values.append(card.value)
        straights = []
        counter = 1
        for index in range(1, len(unique_cards)):
            if unique_cards[index].value == unique_cards[index - 1].value + 1:
                counter += 1
                if counter >= 5:
                    straights.append(unique_cards[index - 4: index + 1])
            else:
                counter = 1
        return straights

    def find_full_houses(self):
        pairs = self.find_n_tuples(2)
        triples = self.find_n_tuples(3)
        if not triples:
            return []
        full = []
        for triple in triples:
            suitable_pairs = [pair for pair in pairs if pair[0].value != triple[0].value]
            if not suitable_pairs:
                return []
            suitable_pairs.sort(key=lambda pair: pair[0].number)
            full.append(triple + suitable_pairs[0])
        return full

    def find_quads(self):
        quads = self.find_exact_n_tuples(4)
        if not quads:
            return []
        potential_kickers = self.find_exact_n_tuples(1)
        if potential_kickers:
            good_kicker = potential_kickers[0]
            return [quad + good_kicker for quad in quads]
        else:
            quad_list = []
            for quad in quads:
                kicker = [card for card in self.cards if card.value != quad[0].value][0]
                quad_list.append(quad + [kicker])
            return quad_list

    def find_straight_flushes(self):
        suits = [[card for card in self.cards if card.suit == i] for i in range(0, 4)]
        straight_flushes = []
        for suit in suits:
            straight_flushes += HandAnalyser(suit).find_straights()
        return straight_flushes

    def find_n_tuples(self, n):
        values = [card.value for card in self.cards]
        suitable_values = {value for value in values if values.count(value) >= n}
        return [[card for card in self.cards if card.value == value][:n] for value in suitable_values]

    def find_exact_n_tuples(self, n):
        values = [card.value for card in self.cards]
        suitable_values = {value for value in values if values.count(value) == n}
        return [[card for card in self.cards if card.value == value] for value in suitable_values]

    def filter_valid(self, possible_plays, last_played_cards):
        return [play for play in possible_plays if CardList(play).is_valid_play(self.cards, last_played_cards)]
