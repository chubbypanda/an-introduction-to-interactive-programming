# Mini-project 5 for An Introduction to Interactive Programming in Python class, by k., 10/25/2014
# "Memory"
# https://class.coursera.org/interactivepython-005/human_grading/view/courses/972530/assessments/32/submissions
# the code runs only in Codeskulptor (obscure Python interpretter for the class)

# template available at http://www.codeskulptor.org/#examples-memory_template.py


import random
import simplegui

# initialize global variables
exposed = []
deck = []
flipped_cards = []
turns = 0

def new_game():
    global deck, exposed, state, turns
    state, turns = 0, 0
    list_a = list_b = range(8)
    deck = list_a + list_b
    random.shuffle(deck)
    # none of the cards are exposed at the beginning
    exposed = [False for dummy_card in deck]
   
# define event handlers
def mouseclick(position):
    global state, flipped_cards, turns
    # determine which card spot have been clicked on, by 50 (width / number of cards)
    spot =  position[0] / (800 / len(deck))

    # add game state logic here
    if not exposed[spot]:
        exposed[spot] = True
    else:
        # this card was already exposed, ignore the mouseclick
        return        
    
    if state == 0:
        # start of the game
        state = 1
        flipped_cards.append(spot)
    elif state == 1:
        # the end of a turn
        state = 2
        # counter incremented after either 1st or 2nd card is flipped during a turn
        turns += 1
        flipped_cards.append(spot)
    else:
        # single exposed unpaired card
        state = 1
        # determine if the previous two cards are paired or unpaired
        if (deck[flipped_cards[0]] != deck[flipped_cards[1]]):
            exposed[flipped_cards[0]], exposed[flipped_cards[1]] = False, False
        # done, reset current two flipped cards
        flipped_cards = []
        flipped_cards.append(spot)
         
# cards are 50*100 pixels in size    
def draw(canvas):
    global exposed
    # draw the number associated with each card on the canvas...
    for item, card in enumerate(deck):
        # ...horizontal sequence evenly-spaced
        canvas.draw_text(str(card), [(50 * item) + 15, 60], 40, 'red')
        # the i-th entry should be True if the i-th card is face up
        if not exposed[item]:
            # width 48 instead of 50 to expose borders between cards
            canvas.draw_line([(50 * item) + 25, 0], [(50 * item) + 25, 100], 48, 'white')

    label.set_text('Turns = ' + str(turns))


# create frame and add a button and labels
frame = simplegui.create_frame('Memory', 800, 100)
frame.add_button('Reset', new_game)
label = frame.add_label('')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
