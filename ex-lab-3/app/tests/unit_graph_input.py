import unittest
import sys
sys.path.append('../')
from data_structures.graph import Graph
from algorithms.utils import *


class TestGraphInput(unittest.TestCase):

    def test_single_file_10(self):
        g = populateGraphFromFile('../dataset/input_random_01_10.txt')
        self.assertEqual(len(g.V), 10)

    def test_single_file_500(self):
        g = populateGraphFromFile('../dataset/input_random_53_500.txt')
        self.assertEqual(len(g.V), 500)

    def test_folder(self):
        gs = loadFromFolder('../dataset/')
        const = 1
        self.assertEqual(len(gs), 56)
        self.assertEqual(len(gs[1-const].V), 10)
        self.assertEqual(len(gs[17-const].V), 80)
        self.assertEqual(len(gs[33-const].V), 250)
        self.assertEqual(len(gs[56-const].V), 500)

    def test_total_vertex_edges(self):
        g = populateGraphFromFile('../dataset/input_random_42_350.txt')
        self.assertEqual(len(g.V), g.totalVertex)
        self.assertEqual(len(g.E), g.totalEdges)

    
    def test_total_vertex_edges_folder(self):
        gs = loadFromFolder('../dataset/')
        for g in gs:
            self.assertEqual(len(g.V), g.totalVertex)
            self.assertEqual(len(g.E), g.totalEdges)


if __name__ == '__main__':
    unittest.main()