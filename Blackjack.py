# Mini-project #6 - Blackjack
#created by FF on 13/05/2014

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com

card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Wana Hit or Stand?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0],
                                                             pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        s = "Hand contains "
        for card in self.hand:
            s += str(card) + " "
        return s
    
    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        global in_play, message, score
        self.value = 0 
        no_ace = True
        for card in self.hand:
            if card.get_rank() == "A":
                no_ace = False
            self.value += VALUES[card.get_rank()]            
        if not (no_ace) and (self.value + 10 <= 21):
            self.value += 10
        if self.value > 21:
            in_play = False                
        return self.value
    
    def draw (self, canvas, pos):
        position = pos
        for card in self.hand:
            card.draw(canvas, position)
            position[0] += 80
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Card object using Card(suit, rank) and add it to the card list for the deck
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
         return self.deck.pop()
        
    def __str__(self):
        # return a string representing the deck
        s = "Deck contains "
        for elem in self.deck:
            s += str(elem) + " "
        return s

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, score
    outcome = "Wana Hit or Stand?"
    if in_play == True:
        outcome = "Not allowed to do another hand before this one isn't over."
        score -= 1
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(0,2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    in_play = True

def hit():
    global in_play, score, outcome
    if in_play == True:
        my_deck = Deck()
        player_hand.add_card(my_deck.deal_card())
        value = player_hand.get_value()
        if value > 21:
            outcome = "You're over the top!"
            score -= 1
    else:
        outcome = "Want another Deal?"
        
def stand():
    
    global in_play, score, outcome  
    dealer_value = dealer_hand.get_value()
    player_value = player_hand.get_value()
    if in_play == False:
        outcome = "Want another Deal?"
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer_value < 17:
            dealer_hand.add_card(deck.deal_card())
            dealer_value = dealer_hand.get_value()
        if dealer_value > 21: 
            score += 1
            outcome = "Player wins."
        elif player_value > dealer_value:
            score += 1
            outcome = "You won."
        else:
            score -= 1
            outcome = "Dealer wins."
        in_play = False

CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)

# draw handler    
def draw(canvas):
    global outcome, in_play
    # drawing player and dealer hand
    dealer_hand.draw(canvas, [40, 200])
    player_hand.draw(canvas, [40, 380])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [40 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

    #Main_title
    Main_title = "BlackJack"
    canvas.draw_text(Main_title, (250,100), 24, "Yellow")
    canvas.draw_text("Your score: " + str(score),
                     [460, 555], 18, "Yellow")
    canvas.draw_text(outcome, [40, 185], 18, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric