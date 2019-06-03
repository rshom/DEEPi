import unittest
from deepi import *

class TestSomething(unittest.TestCase):

    def test_a_funciton(self):
        self.assertAlmostEqual( a_function(inputs), answer)
        self.assertAlmostEqual( a_function(inputs), answer)
        self.assertAlmostEqual( a_function(inputs), answer)
        self.assertAlmostEqual( a_function(inputs), answer)

        #python -m unittest test_a_funcitons
        #python -m unittest
