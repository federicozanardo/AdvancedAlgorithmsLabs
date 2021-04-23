from collections import defaultdict
import sys
sys.path.append('../')

# from data_structures.disjoint_set import DisjointSet
# from data_structures.graph import Graph
# from data_structures.heap import Heap, Node

# class Prim:
#     # Prim(G,s)
#     #     for each u in V do
#     #         key[u] <- inf
#     #         parents(u) <- null
#     #     key[s] <- 0
#     #     Q <- V

#     #     while Q!=empty do
#     #         u <- extractMin(Q)
#     #         for each v adjacent to u do
#     #             if v in Q and w(u,v) < key[v] then
#     #                 parents(v) <- u
#     #                 key[v] <- w(u,v)

#     def prim_mst(self, G, s):
#         # Initialization & Q <- V
#         key = defaultdict(list)
#         parent = defaultdict(list)

#         Q = Heap()

#         for node in G.V:
#             key[node] = 0 if s==node else float('inf')
#             #key.insert(int(node), 0 if s==node else float('inf'))
#             parent[node] = None
#             #parent.insert(int(node), None)
#             Q.insert(Node(node, key[node]))

#         # algoritmo
#         while Q.currentSize != 0:
#             Q.print()
#             u = (Q.extractMin()).toTuple()
#             for (v,w) in G.graph[u[0]]:
#                 print(v)
#                 print(Q.search(v))
#                 if Q.search(v) and w < key[v]:
#                     print(v)
#                     parent[v] = u
#                     key[v] = w
#                     Q.searchAndUpdateWeight(v, key[v])
                
#             print(G.graph[u[0]])
#             print(key)
#         for (x, y) in G.graph[u[0]]:
#             print(x)
#         return key

#     def ahaha(self, G, u, v):
#         minWeight = float('inf')
#         found = False
#         for i in range(len(G.E)):
#             if found: 
#                 break
#             if G.graph[i] == u and G.graph[i] == v: 
#                 minWeight = G.graph[i]
#                 found = True
#         return minWeight


#     def get_weight(self, key):
#         sum = 0
#         for (k, v) in key.items():
#             #print(v)
#             if v!= float('inf'):
#                 sum += v
#         return sum
        

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
        self.areInHeap[node.node] = position # TO CHECK, NEED TO SET 2 ELEMENTS

    def heapifyUp(self, index) :
        while(index > 0):
            element = self.heap[index]
            parentIndex = (index-1) // 2
            parent = self.heap[parentIndex]
            # print(element.weight, "parent weight = ", parent.weight)
            if parent.weight <= element.weight:
                break

            self.areInHeap[(self.heap[parentIndex].node, index)]
            self.heap[index] = parent
            self.heap[parentIndex] = element
            index = parentIndex
        return index

    def extractMin(self):
        minimum = self.heap[0]
        lastElement = self.heap.pop(len(self.heap)-1)

        if(minimum != None):
            del self.areInHeap[minimum.node]
        
        if len(self.heap) != 0:
            self.heap[0] = lastElement
            self.heapifyDown(0)

        return minimum

    def heapifyDown(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        length = len(self.heap)

        print(left, right, smallest, length)

        if left <= length and smallest <= length:
            if self.heap[left] and self.heap[left].weight < self.heap[smallest].weight:
                smallest = left
        if right <= length and smallest <= length:
            if self.heap[right] and self.heap[right].weight < self.heap[smallest].weight:
                smallest = right
        self.areInHeap[self.heap[smallest].node] = index # TO CHECK
        self.areInHeap[self.heap[index].node] = smallest # TO CHECK

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
    key = defaultdict(list)
    parents = defaultdict(list)
    nodes = graph.V

    for node in nodes:
        key[node] = float('inf')
        parents = [node], None

    return key, parents


def createPriorityQueue(graph, key):
    minHeap = MinHeap()
    nodes = graph.V # same as: graph.graph.keys()

    for node in nodes:
        minHeap.insert(HeapNode(node, key[node]))

    return minHeap


class Prim():

    def prim_mst(self, graph, startingNode) :
        key, parents = initialization(graph)
        key[startingNode] = 0

        priorityQueue = createPriorityQueue(graph, key)

        while not priorityQueue.isEmpty():
            current = priorityQueue.extractMin()
            adjacentOfCurrent = graph.graph[current.node]

            for adjNode in adjacentOfCurrent:
                if priorityQueue.contains(adjNode) and graph.weightBetween(current.node, adjNode[0]) < key[adjNode[0]]:
                    parents[adjNode[0]] = current
                    key[adjNode[0]] = graph.weightBetween(current.node, adjNode[0])
                    priorityQueue.update(adjNode[0], key[adjNode[0]])
        return key, parents
    


    def get_weight(self, key):
        sum = 0
        for v in key:
            #print(v)
            if v!= float('inf'):
                sum += v
        return sum
  