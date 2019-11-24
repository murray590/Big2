import pygame
import time

from player import Player
from card_list import CardList
from computer_alex import ComputerAlex
from dealer import Dealer
from config import CONFIG


def display_text(text, size, colour, background, location):
    basic_font = pygame.font.SysFont(None, size)
    words = basic_font.render(text, True, colour, background)
    screen.blit(words, location)


def display_single_card(card, left, top):
    card.left = left
    card.top = top
    card.image = pygame.draw.rect(screen, card.colour, (left, top, card_width, card_height), 0)
    display_text(str(card.pp_value), 60, CONFIG['grey'], card.colour, (left, top))


def choose_cards(hand):
    my_cards = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if play_button.collidepoint(pos):
                    hand.sort(key=lambda card: card.number)
                    my_cards.sort(key=lambda card: card.number)
                    return my_cards
                if any(card.image.collidepoint(pos) for card in hand):
                    selected_card = next((y for y in hand if y.image.collidepoint(pos)), None)
                    pygame.draw.rect(screen, CONFIG['white'], (selected_card.left, selected_card.top, card_width, card_height), 0)
                    selected_card.display(selected_card.left, selected_card.top - card_height / 2)
                    pygame.display.update()
                    my_cards.append(selected_card)
                    hand.remove(selected_card)
                elif any(card.image.collidepoint(pos) for card in my_cards):
                    selected_card = next((y for y in my_cards if y.image.collidepoint(pos)), None)
                    pygame.draw.rect(screen, CONFIG['white'], (selected_card.left, selected_card.top, card_width, card_height), 0)
                    selected_card.display(selected_card.left, selected_card.top + card_height / 2)
                    pygame.display.update()
                    my_cards.remove(selected_card)
                    hand.append(selected_card)
            elif event.type == pygame.QUIT:
                pygame.quit()


def play(some_cards, hand, cards):
    if any(card.number == 0 for card in hand) and not any(card.number == 0 for card in some_cards):
        error("You must include the blue 3 in your play")
        return 1
    else:
        the_cards = CardList(some_cards)
        old_cards = CardList(cards)
        if the_cards.is_valid_quantity(old_cards) and the_cards.is_stronger_than(old_cards):
            display_cards(some_cards, width/2 - 2.5*card_width, height/2 - 0.5*card_height)
            return 0
        else:
            return 2


def repaint(player, cards):
    global play_button
    screen.fill(CONFIG['white'])
    pygame.draw.ellipse(screen, CONFIG['grey'], (width/6, height/4, 2 * width/3, height/2), 0)
    play_button = pygame.draw.rect(screen, CONFIG['grey'], (6*width/7, 3*height/4, 2.1*card_width, 0.5*card_height), 0)
    display_text('Play/pass', 30, CONFIG['purple'], CONFIG['grey'], (6*width/7, 3*height/4))
    display_text(f"Player {player.name}:", 30, CONFIG['purple'], CONFIG['white'], (0, 3*height/4))
    # display_text('Player ' + str(player.next_player(players)) + ':', 30, CONFIG['purple'], CONFIG['white'], (0, 0))
    # display_text(str(len(player.next_player(players).hand)), 30, CONFIG['purple'], CONFIG['grey'], (width/8, 0))
    display_cards(cards, width/2 - 2.5*card_width, height/2 - 0.5*card_height)
    
    
def turn(player, last_played_cards):
    while True:
        repaint(player, last_played_cards)
        display_cards(player.hand, width/32, 6*height/7)
        if hasattr(player, 'computer'):
            time.sleep(1)
            candidate_cards = player.computer.choose_cards(last_played_cards, player.hand)
            if play(candidate_cards, player.hand, last_played_cards) == 0:
                final_cards = candidate_cards
                for card in final_cards:
                    player.hand.remove(card)
            break
        else:
            candidate_cards = choose_cards(player.hand)
            if play(candidate_cards, player.hand, last_played_cards) == 0:
                final_cards = candidate_cards
                break           
            for card in candidate_cards:
                player.hand.append(card)
            player.hand.sort(key=lambda card: card.number)
    return final_cards


def display_cards(cards, left, top):
    n = len(cards)
    for i in range(0, n):
        display_single_card(cards[i], left + i*card_width, top)
    pygame.display.update()


def error(message):
    pass
    # display_text(message, 30, CONFIG['purple'], CONFIG['grey'], (width/10, height/3)).display()
    # pygame.display.update()
    # time.sleep(5)


def message(message):
    display_text(message, 30, CONFIG['purple'], CONFIG['grey'], (width/10, height/3)).display()
    pygame.display.update()
    time.sleep(5)
    
    
def game(players):
    dealer = Dealer(players)
    dealer.deal()
    current_player = dealer.who_starts()
    cards = []
    while True:
        if (all(player.last_played_cards == [] for player in current_player.opponents(players)) and current_player.last_played_cards != []) == True:
            cards = []
        current_player.last_played_cards = turn(current_player, cards)
        if current_player.last_played_cards != []:
            cards = current_player.last_played_cards
        if len(current_player.hand) > 0:
            current_player = current_player.next_player(players)
        else:
            repaint(current_player, cards)
            break
    message(f"Player {current_player.name} is the winner!")

pygame.init()
pygame.display.set_caption('Big2')

width = 800
height = 560
card_width = width/16
card_height = height/8
screen = pygame.display.set_mode((width, height))

A = Player("A", ComputerAlex())
B = Player("B", ComputerAlex())

players = [A, B]

game(players)

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
pygame.quit()
