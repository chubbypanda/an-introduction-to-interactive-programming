# unit tests for Mini-project 1 (Rock-paper-scissors-lizard-Spock), by k., 09/28/2014

import unittest
from mini_project1 import name_to_number
from mini_project1 import number_to_name
from mini_project1 import rpsls


class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass
    def test_names(self):
        self.assertIs(type(name_to_number('rock')), int)
        self.assertEqual(name_to_number('rock'), 0)
        self.assertEqual(name_to_number('Spock'), 1)
        self.assertEqual(name_to_number('paper'), 2)
        self.assertEqual(name_to_number('lizard'), 3)
        self.assertEqual(name_to_number('scissors'), 4)
        self.assertEqual(name_to_number('spock'), -1)
        self.assertEqual(name_to_number('Kirk'), -1)
        self.assertEqual(name_to_number(88), -1)
    def test_numbers(self):
        self.assertIs(type(number_to_name(0)), str)
        self.assertEqual(number_to_name(0), 'rock')
        self.assertEqual(number_to_name(1), 'Spock')
        self.assertEqual(number_to_name(2), 'paper')
        self.assertEqual(number_to_name(3), 'lizard')
        self.assertEqual(number_to_name(4), 'scissors')
        self.assertEqual(number_to_name(-1), -1)
        self.assertEqual(number_to_name(5), -1)
        self.assertEqual(number_to_name(1000), -1)
        self.assertEqual(number_to_name('abc'), -1)
    def test_play(self):
        rpsls('rock')
        print '\nVisually compare with correct answers bellow:'
        print 'Player chooses rock', '\n', 'Computer chooses lizard', \
              '\n', 'Player wins!'
        print '\nPlayer chooses rock', '\n', 'Computer chooses rock', \
              '\n', 'Player and computer tie!'
        print '\nPlayer chooses rock', '\n', 'Computer chooses Spock', \
              '\n', 'Computer wins!'
        print '\nPlayer chooses rock', '\n', 'Computer chooses scissors', \
              '\n', 'Player wins!'
        print '\nPlayer chooses rock', '\n', 'Computer chooses paper', \
              '\n', 'Computer wins!', '\n'

        rpsls('scissors')
        print '\nVisually compare with correct answers bellow or above:'
        print '\nPlayer chooses scissors', '\n', 'Computer chooses paper', \
              '\n', 'Player wins!'
        print '\nPlayer chooses scissors', '\n', 'Computer chooses lizard', \
              '\n', 'Player wins!'
        print '\nPlayer chooses scissors', '\n', 'Computer chooses Spock', \
              '\n', 'Computer wins!', '\n'

        rpsls('lizard')
        print '\nVisually compare with correct answers bellow or above:'
        print '\nPlayer chooses lizard', '\n', 'Computer chooses Spock', \
              '\n', 'Player wins!'
        print '\nPlayer chooses lizard', '\n', 'Computer chooses Paper', \
              '\n', 'Player wins!', '\n'
        
        rpsls('paper')
        print '\nVisually compare with correct answers bellow or above:'
        print '\nPlayer chooses paper', '\n', 'Computer chooses Spock', \
              '\n', 'Player wins!'
        

# let's run it in IDLE
if __name__ == '__main__':
    unittest.main(exit=False)
