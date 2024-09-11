# tests/test_advanced_math.py

import math
import sys
import os
import unittest

# Dynamically add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.advanced_math import sqrt, log, sin, cos, tan, exp

class TestAdvancedMath(unittest.TestCase):
    
    def test_sqrt(self):
        self.assertEqual(sqrt(9), 3)
        with self.assertRaises(ValueError):
            sqrt(-1)
    
    def test_log(self):
        self.assertAlmostEqual(log(1), 0)
        self.assertAlmostEqual(log(10, 10), 1)
        with self.assertRaises(ValueError):
            log(0)
    
    def test_sin(self):
        self.assertAlmostEqual(sin(0), 0)
        self.assertAlmostEqual(sin(math.pi / 2), 1)
    
    def test_cos(self):
        self.assertAlmostEqual(cos(0), 1)
        self.assertAlmostEqual(cos(math.pi), -1)
    
    def test_tan(self):
        self.assertAlmostEqual(tan(0), 0)
        self.assertAlmostEqual(tan(math.pi / 4), 1)
    
    def test_exp(self):
        self.assertAlmostEqual(exp(1), math.e)
        self.assertAlmostEqual(exp(0), 1)

if __name__ == '__main__':
    unittest.main()
