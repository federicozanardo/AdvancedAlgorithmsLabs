from collections import defaultdict

import sys
sys.path.append('../')


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list
        self.V = set()
        self.E = []

    def add_vertex(self, value: int):
        self.V.add(value)
        self.graph[value] = []

    # assunzione: viene chiamato appena dopo gli addVertex
    def add_edge(self, u: int, v: int, w: int):
        self.E.append((u, v, w))
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    def remove_edge(self, u: int, v: int, w: int):
        self.E.remove((u, v, w))
        self.graph[u].remove((v, w))
        self.graph[v].remove((u, w))

    def weightBetween(self, firstNode, secondNode):
        minWeight = float('inf')

        for index in range(0, len(self.E)):
            if (self.E[index][0] == firstNode and self.E[index][1] == secondNode) or (self.E[index][1] == firstNode and self.E[index][0] == secondNode):
                minWeight = self.E[index][2]
                break
        return minWeight
