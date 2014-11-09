# Mini-project 6 for An Introduction to Interactive Programming in Python class, by k., 11/01/2014
# Blackjack
# https://class.coursera.org/interactivepython-005/human_grading/view/courses/972530/assessments/33/submissions
# the code runs only in Codeskulptor (obscure Python interpretter for the class)

# template available at http://www.codeskulptor.org/#examples-blackjack_template.py

import random
import simplegui

# load card sprite, resolution 936*384 (source: jfitz.com)
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image('http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png')

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image('http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png')

# initialize some useful global variables
in_play = False
outcome = ''
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define Card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print 'Invalid card: ', suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_location = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_location, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


# define Hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards_list = []
        self.aces = False

    def __str__(self):
        # return a string representation of a hand
        string = ''
        for item in range(len(self.cards_list)):
            string += str(self.cards_list[item]) + ' '
        return 'Hand contains ' + string

    def add_card(self, card):
        # add a card object to a hand
        self.cards_list.append(card)
        if card.get_rank() == 'A':
            self.aces = True

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see the Blackjack video from class
        value = 0
        for card in self.cards_list:
            value += VALUES[card.get_rank()]
        if self.aces and value <= 11:
            value += 10
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards_list:
            card.draw(canvas, pos)
            pos[0] += 90
        
        
# define Deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards_list.append(Card(suit, rank))
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards_list)

    def deal_card(self):
        return self.cards_list.pop()
    
    def __str__(self):
        # return a string representing the deck
        string = ''
        for item in range(len(self.cards_list)):
            string += str(self.cards_list[item]) + ' '
        return 'Deck contains ' + string


# define event handlers for buttons
def deal():
    global outcome, in_play, dealer, player, deck, message, score

    if (in_play):
        score -= 1
    
    in_play = True
    message = 'Please decide, hit or stand?'
    deck = Deck()
    deck.shuffle()
    
    dealer = Hand()
    player = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())

def hit():
    global outcome, in_play, dealer, player, message, score
    
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            in_play = False
            outcome = 'Player busts, dealer wins.'
            message = 'Deal again?'
            score -= 1
            
       
def stand():
    global outcome, in_play, message, score
    
    if in_play:
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        in_play = False
        message = 'Deal again?'
        # assign a message to outcome, update in_play and score
        if dealer.get_value() > 21:
            outcome = 'Dealer busts, player wins.'
            score += 1
        else:
            if dealer.get_value() >= player.get_value():
                outcome = 'Dealer wins.'
                score -= 1
            else:
                outcome = 'Player wins.'
                score += 1
                
    print dealer.get_value(), dealer
    print player.get_value(), player

# draw handler    
def draw(canvas):
    dealer.draw(canvas, [50, 250])
    player.draw(canvas, [50, 400])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          (50 + (CARD_BACK_SIZE[0] / 2), 250 + (CARD_BACK_SIZE[1] / 2)),
                          CARD_BACK_SIZE)
        
    canvas.draw_text('Blackjack', [80, 140], 40, 'white')
    canvas.draw_text('Score: ' + str(score), [300, 135], 25, 'white')
    canvas.draw_text('Dealer', [80, 230], 25, 'white')
    canvas.draw_text('Player', [80, 380], 25, 'white')
    canvas.draw_text(outcome, [200, 230], 25, 'white')
    canvas.draw_text(message, [200, 380], 25, 'white')

# initialization frame
frame = simplegui.create_frame('Blackjack', 600, 600)
frame.set_canvas_background('green')

#create buttons and canvas callback
frame.add_button('Deal', deal, 200)
frame.add_button('Hit',  hit, 200)
frame.add_button('Stand', stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
