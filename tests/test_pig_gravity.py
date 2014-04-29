import random
import unittest
from pig_gravity import *

class TestPigGravity(unittest.TestCase):

    def setUp(self):
        self.rx = 0.4
        self.ry = 0.4
        self.vector = [self.rx, self.ry]

    def test_decreasing(self):
        rx = 0.01
        ry = 0.01
        gravity = PigGravity(rx, ry)
        self.assertEqual(gravity.affect(self.vector), [0.39, 0.39])

if __name__ == '__main__':
    unittest.main()
