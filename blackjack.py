# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = 0
run = 1 # check the end of game

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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):
        return ' '.join(["%s" %(dummy_str) for dummy_str in self.hand])	# return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        card_values, aces = 0, 0
        for dummy_card in self.hand:
            if dummy_card.get_rank() == 'A':
                aces += VALUES[dummy_card.get_rank()]
            else:
                card_values += VALUES[dummy_card.get_rank()]
        if aces > 0 and card_values + aces + 10 <= 21:
            return card_values + aces + 10
        return card_values + aces	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        global in_play
        if pos == [100, 330]: # player:
            for idx, card in enumerate(self.hand):
                card.draw(canvas, [pos[0] + CARD_CENTER[0]*idx, pos[1]])
        else:
            for idx, card in enumerate(self.hand):
                if idx == 0 and run == 0: # dealer in play and still run
                    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0],
                                                                                    pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE) 
                else:
                    card.draw(canvas, [pos[0] + CARD_CENTER[0]*idx, pos[1]])    
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(dummy_suit, dummy_rank) for dummy_suit in SUITS for dummy_rank in RANKS]	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
        return ' '.join(["%s" %(dummy_str) for dummy_str in self.deck])	# return a string representing the deck



#define event handlers for buttons
def deal():
    global deck, player, dealer, run, score, message, outcome, in_play
    if run == 0:
        score -= 1
    outcome = '^ ^'
    message = ''
    deck = Deck()
    deck.shuffle()
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    run = 0
    in_play = True

def reset():
    """
       reset the score of blackjack game.
       """
    global deck, player, dealer, run, score, message, outcome, in_play
    score = 0
    outcome = '= ='
    message = ''
    deck = Deck()
    deck.shuffle()
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    run = 0
    in_play = True

def hit():
    global deck, player, dealer, run, message, outcome, in_play, score
    if player.get_value() <= 21:
    # if the hand is in play, hit the player
        if in_play: 
            player.add_card(deck.deal_card())
            outcome = "Hit or stand?"
    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        message = "You have busted!"
        outcome = "New deal?"
        if run == 0:
            score -= 1
        run = 1
             
def stand():
    global deck, player, dealer, run, message, outcome, in_play, score
    #  If the player has busted, then remind the player.
    if player.get_value() > 21:
        message = "You have busted!"
        outcome = "New deal?"
    else:
        # check the player and dealer in play
        if in_play:
            in_play = False
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
            while not in_play:
                dealer.add_card(deck.deal_card())
                if dealer.get_value() >= 17:
                    break
        # assign a message to outcome, update in_play and score
        if dealer.get_value() > 21:
            message = "dealer has busted!"
            outcome = "New deal?"
            if run == 0:
                score += 1
            run = 1
        elif dealer.get_value() < player.get_value():
            message = "player wins!"
            outcome = "New deal?"
            if run == 0:
                score += 1
            run = 1
        else:
            message = "dealer wins!"
            outcome = "New deal?"
            if run == 0:
                score -= 1
            run = 1

# draw handler    
def draw(canvas):
    global score, outcome
    canvas.draw_text("player", (100, 300), 20, 'white')
    canvas.draw_text(outcome, (200, 300), 20, 'white')
    player.draw(canvas, [100, 330])
    canvas.draw_text("dealer", (100, 100), 20, 'white')
    canvas.draw_text(message, (200, 100), 20, 'white')
    dealer.draw(canvas, [100, 130])
    canvas.draw_text("Game score : "+str(score), (300, 50), 40, 'white')
    canvas.draw_text("Blackjack", (50, 50), 40, 'white')
    
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset", reset, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric