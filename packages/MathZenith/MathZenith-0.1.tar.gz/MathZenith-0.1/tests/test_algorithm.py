# tests/test_algorithms.py
import sys
import os
import unittest

# Dynamically add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.algorithm import binary_search, bubble_sort, insertion_sort, selection_sort

class TestAlgorithm(unittest.TestCase):
    
    def test_binary_search(self):
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 3), 2)
        self.assertEqual(binary_search([1, 2, 3, 4, 5], 6), -1)
    
    def test_bubble_sort(self):
        self.assertEqual(bubble_sort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])
    
    def test_insertion_sort(self):
        self.assertEqual(insertion_sort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])
    
    def test_selection_sort(self):
        self.assertEqual(selection_sort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])

if __name__ == '__main__':
    unittest.main()
