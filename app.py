import random
import math
import pygame
import time

from player import Player
from card_list import CardList


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


class Text:
    def __init__(self, text, size, colour, background, location):
        self.text = text
        self.size = size
        self.colour = colour
        self.location = location
        self.background = background

    def display(self):
        basic_font = pygame.font.SysFont(None, self.size)
        words = basic_font.render(self.text, True, self.colour, self.background)
        screen.blit(words, self.location)


class Card:
    def __init__(self, number):
        self.number = number
        self.suit = number % 4
        self.value = math.floor(number/4)
        self.value_to_pp = {12: 2, 11: 'A', 10: 'K', 9: 'Q', 8: 'J'}
        self.pp_value = self.value_to_pp[self.value] if self.value in self.value_to_pp else self.value + 3
        self.suit_to_colour = {0: blue, 1: green, 2: red, 3: black}
        self.colour = self.suit_to_colour[self.suit]

    def display(self, left, top):
        self.left = left
        self.top = top
        self.image = pygame.draw.rect(screen, self.colour, (left, top, card_width, card_height), 0)
        Text(str(self.pp_value), 60, grey, self.colour, (left, top)).display()


def deal(some_players):
    num_players = len(some_players)
    num_hands = num_players * 2 if num_players == 2 else num_players
    random.shuffle(deck)
    for index in range(0, num_players):
        some_players[index].hand = sorted(deck[int(index * (52 / num_hands)):int((index + 1) * (52 / num_hands))], key=lambda card: card.number)


def who_starts(some_players):
    lowest_card_numbers = [player.hand[0].number for player in some_players]
    min_card = min(lowest_card_numbers)
    for p in some_players:
        if any(card.number == min_card for card in p.hand):
            return p


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
                    pygame.draw.rect(screen, white, (selected_card.left, selected_card.top, card_width, card_height), 0)
                    selected_card.display(selected_card.left, selected_card.top - card_height / 2)
                    pygame.display.update()
                    my_cards.append(selected_card)
                    hand.remove(selected_card)
                elif any(card.image.collidepoint(pos) for card in my_cards):
                    selected_card = next((y for y in my_cards if y.image.collidepoint(pos)), None)
                    pygame.draw.rect(screen, white, (selected_card.left, selected_card.top, card_width, card_height), 0)
                    selected_card.display(selected_card.left, selected_card.top + card_height / 2)
                    pygame.display.update()
                    my_cards.remove(selected_card)
                    hand.append(selected_card)
            elif event.type == pygame.QUIT:
                pygame.quit()


def quantity_checker(my_cards, cards):
    if len(my_cards) == 0 or len(cards) == 0:
        return 0
    elif len(my_cards) > 5:
        error('You must select at most 5 cards!')
        return 1
    elif len(my_cards) != len(cards):
        error('You must select the same number of cards as the previous play!')
        return 2
    else:
        return 0


def play(some_cards, hand, cards):
    if any(card.number == 0 for card in hand) and not any(card.number == 0 for card in some_cards):
        error("You must include the blue 3 in your play")
        return 1
    else:
        if quantity_checker(some_cards, cards) == 0 and CardList(some_cards).is_stronger_than(CardList(cards)):
            display_cards(some_cards, width/2 - 2.5*card_width, height/2 - 0.5*card_height)
            return 0
        else:
            return 2


def repaint(player, cards):
    global play_button
    screen.fill(white)
    pygame.draw.ellipse(screen, grey, (width/6, height/4, 2 * width/3, height/2), 0)
    play_button = pygame.draw.rect(screen, grey, (6*width/7, 3*height/4, 2.1*card_width, 0.5*card_height), 0)
    Text('Play/pass', 30, purple, grey, (6*width/7, 3*height/4)).display()
    Text(f"Player {player.name}:", 30, purple, white, (0, 3*height/4)).display()
    # Text('Player ' + str(player.next_player(players)) + ':', 30, purple, white, (0, 0)).display()
    # Text(str(len(player.next_player(players).hand)), 30, purple, grey, (width/8, 0)).display()
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
        cards[i].display(left + i*card_width, top)
    pygame.display.update()


def error(message):
    pass
    # Text(message, 30, purple, grey, (width/10, height/3)).display()
    # pygame.display.update()
    # time.sleep(5)


def message(message):
    Text(message, 30, purple, grey, (width/10, height/3)).display()
    pygame.display.update()
    time.sleep(5)


def count_n_tuples(hand, n):
    values = []
    for card in hand:
        values.append(card.value)
    ls = []
    for card in values:
        if values.count(card) == n and card not in ls:
            ls.append(card)
    return len(ls)
    
    
def game(players):
    deal(players)
    current_player = who_starts(players)
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

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
grey = (180, 180, 180)

deck = []
for i in list(range(0, 52)):
    deck.append(Card(i))

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
