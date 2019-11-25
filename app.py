import time

# from core.card import Card
from core.card_list import CardList
from core.hand import Hand
from core.player import Player
from core.dealer import Dealer
from outputters.graphics import Graphics
from outputters.printer import Printer
from bots.alex_bot import AlexBot


class App:
    def __init__(self, players):
        self.players = players
        self.printer = (
            Printer()
            if all(hasattr(player, "bot") for player in self.players)
            else Graphics(800, 560)
        )
        self.game()

    def turn(self, player, last_played_cards):
        while True:
            self.printer.display_player(player, last_played_cards.cards)
            self.printer.display_cards(
                player.hand, self.printer.width / 32, 6 * self.printer.height / 7
            )
            time.sleep(1)
            chosen_cards = (
                player.bot.choose_cards(last_played_cards, player.hand)
                if hasattr(player, "bot")
                else self.printer.choose_cards(player.hand)
            )
            candidate_cards = CardList(chosen_cards)
            if candidate_cards.is_valid_play(player.hand, last_played_cards):
                self.printer.display_cards(
                    candidate_cards.cards,
                    self.printer.width / 2 - 2.5 * self.printer.card_width,
                    self.printer.height / 2 - 0.5 * self.printer.card_height,
                )
                for card in candidate_cards.cards:
                    player.hand.remove(card)
                player.hand.sort(key=lambda card: card.number)
                return candidate_cards

    def game(self):
        dealer = Dealer(self.players)
        dealer.deal()
        current_player = dealer.who_starts()
        cards = CardList([])
        while True:
            if (
                all(
                    player.last_played_cards.type == Hand.PASS
                    for player in current_player.opponents(self.players)
                )
                and current_player.last_played_cards.type != Hand.PASS
            ):
                cards = CardList([])
            current_player.last_played_cards = self.turn(current_player, cards)
            if current_player.last_played_cards.type != Hand.PASS:
                cards = current_player.last_played_cards
            if len(current_player.hand) > 0:
                current_player = current_player.next_player(self.players)
            else:
                self.printer.display_player(current_player, cards.cards)
                break
        self.printer.display_message(f"Player {current_player.name}, wielding {current_player.bot.name}, is the winner!")


if __name__ == "__main__":
    App([Player("A", AlexBot()), Player("B", AlexBot())])
    # a = AlexBot()
    # hand = [Card(i) for i in range(0, 18)]
    # print(hand)
    # print(a.is_there_a_flush(hand))
