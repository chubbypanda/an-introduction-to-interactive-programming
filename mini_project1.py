# Mini-project 1 for An Introduction to Interactive Programming in Python class, by k., 09/28/2014
# Rock-paper-scissors-lizard-Spock
# https://class.coursera.org/interactivepython-005/human_grading/view/courses/972530/assessments/28/submissions

# based on the template from: http://www.codeskulptor.org/#examples-rpsls_template.py

# the key idea of this program is to equate the strings 'rock', 'paper', 'scissors', 'lizard', 'Spock'
# to numbers as follows:
#
# 0 - rock; 1 - Spock; 2 - paper; 3 - lizard; 4 - scissors


import random

# helper functions

def name_to_number(name):
    '''
    converts the string name into a number between 0 and 4 as described above
    '''
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print name, 'is not a valid input name!'
        return -1


def number_to_name(number):
    '''
    converts a number in the range 0 to 4 into its corresponding name as a string
    '''
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        print number, 'is not a valid input number!'
        return -1


def rpsls(player_choice):
    '''
    main body for Rock-paper-scissors-lizard-Spock
    '''
    # print a blank line to separate consecutive games
    print ''
    # print out the message of the player's choice
    print 'Player chooses', player_choice

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)

    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print 'Computer chooses', comp_choice

    # compute difference of comp_number and player_number modulo five
    difference = (comp_number - player_number) % 5

    # use if/elif/else to determine winner, print a message
    if difference == 0:
        print 'Player and computer tie!'
    elif difference >= 3:
        print 'Player wins!'
    else:
        print 'Computer wins!'
        

# test your code (following calls must be present in code submitted for grading)
##rpsls('rock')
##rpsls('Spock')
##rpsls('paper')
##rpsls('lizard')
##rpsls('scissors')
