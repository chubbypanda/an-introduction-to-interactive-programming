# Mini-project 2 for An Introduction to Interactive Programming in Python class, by k., 10/04/2014
# "Guess the number" game
# https://class.coursera.org/interactivepython-005/human_grading/view/courses/972530/assessments/29/submissions
# the code runs only in Codeskulptor (obscure Python interpretter for the class)

# input will come from buttons and an input field
# all output for the game will be printed in the console
# template available at http://www.codeskulptor.org/#examples-guess_the_number_template.py


import math
import random

import simplegui

# abudance of global variables (forced onto), don't do this in real life!

# helper function to start and restart the game
def new_game():
    global secret_number 
    secret_number = random.randrange(0, range_end)

# define event handlers for control panel
def range100():
    '''button that changes the range to [0, 100) and starts a new game'''
    global range_end
    range_end = 100
    global count
    # calculated from relation 2 ** n >= high - low + 1
    count = int(math.ceil(math.log(range_end, 2)))
    
    print 'New game. Range is from 0 to', range_end
    print 'Number of remaining guesses is', count, '\n'
    new_game()

def range1000():
    '''button that changes the range to [0, 1000) and starts a new game'''
    global range_end
    range_end = 1000
    global count
    # calculated from relation 2 ** n >= high - low + 1
    count = int(math.ceil(math.log(range_end, 2)))
    
    print 'New game. Range is from 0 to', range_end
    print 'Number of remaining guesses is', count, '\n'
    new_game()
    
def input_guess(guess):
    guess = int(guess)
    print 'Guess was', guess
    global count
    count -= 1
    print 'Number of remaining guesses is', count
    
    if secret_number == guess:
        # correct guess, immediately begin new game in the same range
        print 'Correct!\n'
        if range_end == 100:
            range100()
        else:
            range1000()
    elif secret_number < guess:
        print 'Lower!\n'
    else:
        print 'Higher!\n'
    
    # ran out, immediately begin new game in the same range
    if count == 0:
        print 'You ran out of guesses. The number was', secret_number, '\n'
        if range_end == 100:
            range100()
        else:
            range1000()
   
   
# create frame
frame = simplegui.create_frame('"Guess the Number" game', 200, 200)

# register event handlers for control elements and start frame
frame.add_input('Your guess:', input_guess, 150)
frame.add_button('Range: 0 - 100', range100, 150)
frame.add_button('Range: 0 - 1000', range1000, 150)

range100()
