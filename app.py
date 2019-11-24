import time

from core.card_list import CardList
from core.hand import Hand
from core.player import Player
from core.dealer import Dealer
from core.graphics import Graphics
from core.printer import Printer
from computers.computer_alex import ComputerAlex


class App:
    def __init__(self, players):
        self.players = players
        self.printer = Printer() if all(hasattr(player, 'computer') for player in self.players) else Graphics(800, 560)
        self.game()

    def turn(self, player, last_played_cards):
        while True:
            self.printer.repaint(player, last_played_cards.cards)
            self.printer.display_cards(player.hand, self.printer.width/32, 6 * self.printer.height/7)
            time.sleep(1)
            chosen_cards = player.computer.choose_cards(last_played_cards, player.hand) if hasattr(player, 'computer') else self.printer.choose_cards(player.hand)
            candidate_cards = CardList(chosen_cards)
            if candidate_cards.is_valid_play(player.hand, last_played_cards):
                self.printer.display_cards(candidate_cards.cards, self.printer.width/2 - 2.5*self.printer.card_width, self.printer.height/2 - 0.5*self.printer.card_height)
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
            if (all(player.last_played_cards.type == Hand.PASS for player in
                    current_player.opponents(self.players)) and current_player.last_played_cards != Hand.PASS):
                cards = CardList([])
            current_player.last_played_cards = self.turn(current_player, cards)
            if current_player.last_played_cards.type != Hand.PASS:
                cards = current_player.last_played_cards
            if len(current_player.hand) > 0:
                current_player = current_player.next_player(self.players)
            else:
                self.printer.repaint(current_player, cards.cards)
                break
        self.printer.message(f"Player {current_player.name} is the winner!")


App([Player("A", ComputerAlex()), Player("B", ComputerAlex())])
