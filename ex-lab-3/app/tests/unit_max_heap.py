import unittest
import sys
sys.path.append('../')
from data_structures.max_heap import MaxHeap, Node


class TestMaxHeap(unittest.TestCase):

    def test_creation(self):
        heap = MaxHeap()
        self.assertEqual(heap.currentSize, 0)

    def test_insert(self):
        heap = MaxHeap()
        heap.insert(Node(1, 5))
        heap.insert(Node(2, 7))
        heap.insert(Node(3, 4))
        heap.insert(Node(4, 5))
        heap.insert(Node(5, 9))
        self.assertEqual(heap.currentSize, 5)

    def test_extractMax(self):
        heap = MaxHeap()
        heap.insert(Node(1, 5))
        heap.insert(Node(2, -7))
        heap.insert(Node(3, 4))
        heap.insert(Node(4, -5))
        heap.insert(Node(5, 9))
        heap.insert(Node(6, 2))
        heap.insert(Node(7, 1))
        self.assertEqual(heap.extractMax().weight, 9)
        self.assertEqual(heap.extractMax().weight, 5)
        self.assertEqual(heap.extractMax().weight, 4)
        self.assertEqual(heap.extractMax().weight, 2)
        self.assertEqual(heap.extractMax().weight, 1)
        self.assertEqual(heap.extractMax().weight, -5)
        self.assertEqual(heap.extractMax().weight, -7)


    def test_heapComposition(self):
        heap = MaxHeap()
        heap.insert(Node(1, 30))
        heap.insert(Node(5, 120))
        heap.insert(Node(5, 40))
        heap.insert(Node(5, 50))
        nodel = heap.left(1)
        noder = heap.right(1)
        self.assertEqual(nodel.weight, 50)
        self.assertEqual(noder.weight, 40)
        self.assertEqual(heap.left(2).weight, 30)
        self.assertEqual(heap.extractMax().weight, 120)


if __name__ == '__main__':
    unittest.main()