# unit tests for format converter from Mini-project 3 ("Stopwatch: The Game"), by k., 09/28/2014

import unittest
from time_to_string import format


class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass
    def test_format(self):
        self.assertIs(type(format(620)), str)
        self.assertEqual(format(0), '0:00.0')
        self.assertEqual(format(11), '0:01.1')
        self.assertEqual(format(321), '0:32.1')
        self.assertEqual(format(613), '1:01.3')
        self.assertEqual(format(5999), '9:59.9')       


# let's run it in IDLE
if __name__ == '__main__':
    unittest.main(exit=False)
