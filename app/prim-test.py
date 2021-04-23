
from collections import defaultdict
import sys

class HeapNode():

    def __init__(self,n,w): 
        self.node = n
        self.weight = w

class MinHeap():

    def __init__(self): 
        self.heap = []
        self.areInHeap = defaultdict(list)

    def getMin(self):
        return self.heap[0]

    def insert(self, node):
        self.heap.append(node)
        position = self.heapifyUp(len(self.heap)-1)
        self.areInHeap[(node.node, position)] # TO CHECK, NEED TO SET 2 ELEMENTS

    def heapifyUp(self, index) :
        while(index > 0):
            element = self.heap[index]
            parentIndex = (index-1) // 2
            parent = self.heap[parentIndex]

            if parent.weight <= element.weight:
                break

            self.areInHeap[(self.heap[parentIndex].node, index)]
            self.heap[index] = parent
            self.heap[parentIndex] = element
            index = parentIndex
        return index

    def extractMin(self):
        minimum = self.heap[0]
        lastElement = self.heap.remove(len(self.heap)-1)
        if(minimum != None):
            self.areInHeap.pop(minimum.node)
        
        if len(self.heap) != 0:
            self.heap[0] = lastElement
            self.heapifyDown(0)

        return minimum

    def heapifyDown(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        length = len(self.heap)
        if left <= length and self.heap[left] and self.heap[left].weight < self.heap[smallest].weight:
            smallest = left
        if right <= length and self.heap[right] and self.heap[right].weight < self.heap[smallest].weight:
            smallest = right
        self.areInHeap[(self.heap[smallest].node, index)] # TO CHECK
        self.areInHeap[(self.heap[index].node, smallest)] # TO CHECK

        if smallest != index:
            self.heap[smallest], self.heap[index] = self.heap[index],self.heap[smallest]
            self.heapifyDown(smallest)

    def contains(self, node) :
        return node in self.areInHeap

    def update(self, node, weight):
        index = self.areInHeap.get(node)
        self.heap[index].weight = float('-inf')
        self.heapifyUp(index)
        self.heap[0].weight = weight
        self.heapifyDown(0)

    def isEmpty(self):
        return len(self.heap) == 0



def initialization(graph):
    key = []
    parents = []
    nodes = graph.V

    for node in nodes:
        key[node] = float('inf')
        parents[node] = None

    return key, parents


def createPriorityQueue(graph, key):
    minHeap = MinHeap()
    nodes = graph.graph.keys()

    for node in nodes:
        minHeap.insert(HeapNode(node, key[node]))

    return minHeap


def prim_mst(graph, startingNode) :
    key, parents = initialization(graph)
    key[startingNode] = 0

    priorityQueue = createPriorityQueue(graph, key)

    while not priorityQueue.isEmpty():
        current = priorityQueue.extractMin()
        adjacentOfCurrent = graph.graph[current[0]]

        for adjNode in adjacentOfCurrent:
            if priorityQueue.contains(adjNode) and graph.weightBetween(current.node, adjNode[0]) < key[adjNode[0]]:
                parents[adjNode[0]] = current
                key[adjNode[0]] = graph.weightBetween(current.node, adjNode[0])
                priorityQueue.update(adjNode[0], key[adjNode[0]])
    return key, parents
    
