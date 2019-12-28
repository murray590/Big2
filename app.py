import time

from core.card import Card
from bots.stupid_bot import StupidBot
from core.card_list import CardList
from core.hand_type import HandType
from core.player import Player
from core.dealer import Dealer
from outputters.graphics import Graphics
from outputters.printer import Printer
from bots.alex_bot import AlexBot
from bots.hand_analyser import HandAnalyser


class App:
    def __init__(self, players):
        self.players = players
        self.outputter = (
            Printer()
            if all(player.bot is not None for player in self.players)
            else Graphics(800, 560)
        )
        self.game()

    def turn(self, player, last_played_cards):
        while True:
            self.outputter.display_player(player, last_played_cards.cards)
            self.outputter.display_cards(
                player.hand, self.outputter.width / 32, 6 * self.outputter.height / 7
            )
            time.sleep(1)
            chosen_cards = (
                player.bot.choose_cards(last_played_cards, player.hand)
                if player.bot is not None
                else self.outputter.choose_cards(player.hand)
            )
            candidate_cards = CardList(chosen_cards)
            if candidate_cards.is_valid_play(player.hand, last_played_cards):
                self.outputter.display_cards(
                    candidate_cards.cards,
                    self.outputter.width / 2 - 2.5 * self.outputter.card_width,
                    self.outputter.height / 2 - 0.5 * self.outputter.card_height,
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
                    player.last_played_cards.type == HandType.PASS
                    for player in current_player.opponents(self.players)
                )
                and current_player.last_played_cards.type != HandType.PASS
            ):
                cards = CardList([])
            current_player.last_played_cards = self.turn(current_player, cards)
            if current_player.last_played_cards.type != HandType.PASS:
                cards = current_player.last_played_cards
            if len(current_player.hand) > 0:
                current_player = current_player.next_player(self.players)
            else:
                self.outputter.display_player(current_player, cards.cards)
                break
        self.outputter.display_message(f"Player {current_player.name}, wielding {current_player.bot.name}, is the winner!")


if __name__ == "__main__":
    # App([Player("A", StupidBot()), Player("B", AlexBot())])
    dealer = Dealer([Player("A", None), Player("B", None)])
    dealer.deal()
    print(HandAnalyser(dealer.players[0].hand).find_possible_plays(CardList([])))
    #print(HandAnalyser([Card(i) for i in range(0, 18)]).find_possible_plays(CardList([])))
    print(dealer.players[0].hand)
