
import math
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
            self.ppSuit = 'D'
        elif self.suit == 1:
            self.ppSuit = 'C'
        elif self.suit == 2:
            self.ppSuit = 'H'
        else:
            self.ppSuit = 'S'


deck = []
for i in list(range(0,52)):
    deck.append(Card(i))


test_hand = [Card(0),Card(4),Card(8),Card(12),Card(16),Card(12),Card(20),Card(25),Card(33),Card(37),Card(41),Card(49),Card(51)]


# prints suits of available flushes
def flush_checker(hand):
    suit_values = [i.suit for i in hand]
    for suit in range(0,4):
        if suit_values.count(suit) >= 5:
            print(suit)

#flush_checker(test_hand)


def value(quintuple):
    va = []
    for card in quintuple:
        va.append(card.value - quintuple[0].value)
    return va


# Counts pairs, triples etc
def countNTuples(hand,N):
    values=[]
    for card in hand:
        values.append(card.value)
    ls=[]
    for card in values:
        if values.count(card) == N and card not in ls:
            ls.append(card)
    return len(ls)



#prints stupid message if it finds a straight
def straight_checker(hand):
    if len(hand) < 5 :
        return
        
    for i in range(0,len(hand) - 4):
        if value(hand[i:i+5]) == [0,1,2,3,4]:
            print("there's a straight!")
            
        

straight_checker(test_hand)
