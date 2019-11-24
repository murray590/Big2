import time

from core.card_list import CardList
from core.hand import Hand
from core.player import Player
from computers.computer_alex import ComputerAlex
from core.dealer import Dealer
from core.graphics import Graphics

graphics = Graphics(800, 560)


def turn(player, last_played_cards):
    while True:
        graphics.repaint(player, last_played_cards.cards)
        graphics.display_cards(player.hand, graphics.width/32, 6 * graphics.height/7)
        time.sleep(1)
        candidate_cards = player.computer.choose_cards(last_played_cards, player.hand) if hasattr(player, 'computer') else graphics.choose_cards(player.hand)
        if candidate_cards.is_valid_play(player.hand, last_played_cards):
            graphics.display_cards(candidate_cards.cards, graphics.width/2 - 2.5*graphics.card_width, graphics.height/2 - 0.5*graphics.card_height)
            for card in candidate_cards.cards:
                player.hand.remove(card)
            player.hand.sort(key=lambda card: card.number)
            return candidate_cards

    
def game(players):
    dealer = Dealer(players)
    dealer.deal()
    current_player = dealer.who_starts()
    cards = CardList([])
    while True:
        if (all(player.last_played_cards.type == Hand.PASS for player in
                current_player.opponents(players)) and current_player.last_played_cards != Hand.PASS):
            cards = CardList([])
        current_player.last_played_cards = turn(current_player, cards)
        if current_player.last_played_cards != Hand.PASS:
            cards = current_player.last_played_cards
        if len(current_player.hand) > 0:
            current_player = current_player.next_player(players)
        else:
            graphics.repaint(current_player, cards)
            break
    graphics.message(f"Player {current_player.name} is the winner!")


A = Player("A", ComputerAlex())
B = Player("B", ComputerAlex())

players = [A, B]

game(players)
