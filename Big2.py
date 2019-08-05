import random

players = ["A","B","C","D"]
a = []
b = []
c = []
d = []
starting_player = "E"

suit = {
	1:"Diamonds",
	2:"Clubs",
	3:"Hearts",
	4:"Spades"
	}

value = {
        3:3,
	4:4,
	5:5,
	6:6,
	7:7,
	8:8,
	9:9,
	10:10,
	11:"Jack",
	12:"Queen",
	13:"King",
	14:"Ace",
	15:2
	}

hand = {
	"A":a,
	"B":b,
	"C":c,
	"D":d
	}

def deal():
    global a,b,c,d
    n = list(range(3,16))
    s = list(range(1,5))
    deck = [(x,y) for x in n for y in s]
    random.shuffle(deck)
    a = sorted(deck[:13])
    b = sorted(deck[13:26])
    c = sorted(deck[26:39])
    d = sorted(deck[-13:])

def who_starts():
    global starting_player
    for p in players:
        if (3,1) in hand[p]:
            starting_player = p

def show_hand(player):
    for card in hand[player]:
        print(str(value[card[0]]) + " of " + str(suit[card[1]]))

deal()
who_starts()
show_hand(starting_player)
