import random
import math
import pygame
import time

class Player:
    def __init__(self,x):
                self.hand = []
                self.foot = []
                self.name = x
    def __repr__(self):
        return self.name
    def opponents(self,people):
        opponents = list(people)
        opponents.remove(self)
        return opponents
    def next_player(self,people):
        return people[(people.index(self) + 1) % len(people)]

class Text:
    def __init__(self,text,size,colour,background,location):
                self.text = text
                self.size = size
                self.colour = colour
                self.location = location
                self.background = background
    def display(self):
        basicFont = pygame.font.SysFont(None, self.size)
        words = basicFont.render(self.text, True, self.colour, self.background)
        screen.blit(words,self.location)

class Card:
    def __init__(self,number):
        self.number = number
        self.suit = number % 4
        self.value = math.floor(number/4)
        if self.value == 12:
            self.ppValue = 2
        elif self.value == 11:
            self.ppValue = 'A'
        elif self.value == 10:
            self.ppValue = 'K'
        elif self.value == 9:
            self.ppValue = 'Q'
        elif self.value == 8:
            self.ppValue = 'J'
        else:
            self.ppValue = self.value + 3
        if self.suit == 0:
            self.colour = blue
        elif self.suit == 1:
            self.colour = green
        elif self.suit == 2:
            self.colour = red
        elif self.suit == 3:
            self.colour = black
        else:
            self.colour = white

    def display(self,left,top):
        self.left = left
        self.top = top
        self.image = pygame.draw.rect(screen,self.colour,(left,top,cardWidth,cardHeight),0)
        Text(str(self.ppValue), 60, grey, self.colour, (left, top)).display()

def deal(some_players):
    num_players = len(some_players)
    num_hands = num_players * 2 if num_players == 2 else num_players
    random.shuffle(deck)
    for i in range(0, num_players):
        some_players[i].hand = sorted(deck[int(i*(52/num_hands)):int((i+1)*(52/num_hands))], key=lambda card: card.number)

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
                if playButton.collidepoint(pos):
                    hand.sort(key=lambda card: card.number)
                    my_cards.sort(key=lambda card: card.number)
                    return my_cards
                if any(card.image.collidepoint(pos) for card in hand):
                    selectedCard = next((y for y in hand if y.image.collidepoint(pos)), None)
                    pygame.draw.rect(screen,white,(selectedCard.left,selectedCard.top,cardWidth,cardHeight),0)
                    selectedCard.display(selectedCard.left,selectedCard.top - cardHeight/2)
                    pygame.display.update()
                    my_cards.append(selectedCard)
                    hand.remove(selectedCard)
                elif any(card.image.collidepoint(pos) for card in my_cards):
                    selectedCard = next((y for y in my_cards if y.image.collidepoint(pos)), None)
                    pygame.draw.rect(screen,white,(selectedCard.left,selectedCard.top,cardWidth,cardHeight),0)
                    selectedCard.display(selectedCard.left,selectedCard.top + cardHeight/2)
                    pygame.display.update()
                    my_cards.remove(selectedCard)
                    hand.append(selectedCard)
            elif event.type == pygame.QUIT:
                pygame.quit()

def value(quintuple):
    va = []
    for card in quintuple:
        va.append(card.value - quintuple[0].value)
    return va

def suit(quintuple):
    su = []
    for card in quintuple:
        su.append(card.suit)
    return su

def rank(fiveCards):
    if fiveCards == []:
        return 0
    else:
        v = value(fiveCards)
        s = suit(fiveCards)
        if v == [0,1,2,3,4]:
            if s[0] == s[1] == s[2] == s[3] == s[4]:
                return 5
            else:
                return 1
        elif s[0] == s[1] == s[2] == s[3] == s[4]:
            return 2
        elif (v[0] == v[1]) and (v[3] == v[4]) and (v[2] == v[1] or v[2] == v[3]):
            return 3
        elif (v[0] == v[1] == v[2] == v[3]) or (v[1] == v[2] == v[3] == v[4]):
            return 4
        else:
            return -1

def value_checker(my_cards,last_cards):
    if len(my_cards) == 0:
        return 0
    elif len(my_cards) == 1:
        if len(last_cards) == 0 or my_cards[0].number > last_cards[0].number:
            return 0
        else:
            error("You must play a higher card than the previous play!")
            return 1
    elif len(my_cards) == 2:
        if my_cards[0].value != my_cards[1].value:
            error("A two card play must be a pair!")
            return 2
        elif len(last_cards) == 0 or my_cards[1].number > last_cards[1].number:
            return 0
        else:
            error("You must play a higher pair than the previous play!")
            return 3
    elif len(my_cards) == 3:
        if not (my_cards[0].value == my_cards[1].value == my_cards[2].value):
            error("A three card play must be a three of a kind!")
            return 4
        elif len(last_cards) == 0 or my_cards[2].number > last_cards[2].number:
            return 0
        else:
            error("You must play a higher three of a kind than the previous play!")
            return 5
    elif len(my_cards) == 4:
        error("There is no valid four card play, a four of a kind must be played with a kicker!")
        return 6
    elif len(my_cards) == 5:
        if rank(my_cards) < rank(last_cards):
            if rank(my_cards) == -1:
                error("Invalid hand, try again!")
                return 7
            else:
                error("You need to play a stronger hand!")
                return 8
        if rank(my_cards) > rank(last_cards):
            return 0
        if rank(my_cards) == rank(last_cards):
            if rank(my_cards) == 2 or rank(my_cards) == 5:
                if my_cards[0].suit > last_cards[0].suit:
                    return 0
                elif my_cards[0].suit < last_cards[0].suit:
                    error("You need to play a higher suit!")
                    return 9
            if my_cards[4].number > last_cards[4].number:
                return 0
            else:
                error("You need to play a better hand!")
                return 10


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
        if quantity_checker(some_cards,cards) == 0 and value_checker(some_cards,cards) == 0:
            display_cards(some_cards,width/2 - 2.5*cardWidth,height/2 - 0.5*cardHeight)
            return 0
        else:
            return 2


def repaint(player,cards):
    global playButton
    screen.fill(white)
    pygame.draw.ellipse(screen, grey, (width/6, height/4, 2 * width/3, height/2), 0)
    playButton = pygame.draw.rect(screen,grey,((6*width)/7,(3*height)/4,2.1*cardWidth,0.5*cardHeight),0)
    Text('Play/pass',30,purple,grey,((6*width)/7, (3*height)/4)).display()
    Text('Player ' + str(player) + ':', 30, purple, white, (0, (3*height)/4)).display()
    #Text('Player ' + str(player.next_player(players)) + ':', 30, purple, white, (0, 0)).display()
    #Text(str(len(player.next_player(players).hand)), 30, purple, grey, (width/8, 0)).display()
    display_cards(cards,width/2 - 2.5*cardWidth,height/2 - 0.5*cardHeight)
    
    
def turn(player, last_played_cards):
    while True:
        repaint(player, last_played_cards)
        display_cards(player.hand, width/32, (6*height)/7)
        if player in computers:
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
        cards[i].display(left + (i*cardWidth), top)
    pygame.display.update()


def error(message):
    pass
#    Text(message, 30, purple, grey, (width/10, height/3)).display()
#    pygame.display.update()
#    time.sleep(5)


class ComputerAlex:
    @staticmethod
    def choose_cards(last_cards, hand):
        n = len(hand)
        l = len(last_cards)
        selected_cards = []
        if l == 0:
            selected_cards.append(hand[0])
            return selected_cards
        elif l > 3:
            return selected_cards
        else:
            for i in range(0, n - l + 1):
                selected_cards = hand[i:i+l]
                if play(selected_cards, hand, last_cards) == 0:
                    return selected_cards
                else:
                    selected_cards = []
        return selected_cards


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
        if (all(player.foot == [] for player in current_player.opponents(players)) and current_player.foot != []) == True:
            cards = []
        current_player.foot = turn(current_player,cards)
        if current_player.foot != []:
            cards = current_player.foot
        if len(current_player.hand) > 0:
            current_player = current_player.next_player(players)
        else:
            repaint(current_player, cards)
            break
    error('Player ' + str(current_player) + ' is the winner!')

pygame.init()
pygame.display.set_caption('Big2')

width = 800
height = 560
cardWidth = width/16
cardHeight = height/8
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

A = Player("A")
B = Player("B")
A.computer = ComputerAlex()
B.computer = ComputerAlex()

players = [A, B]
computers = [player for player in players if hasattr(player, 'computer')]

game(players)

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
pygame.quit()