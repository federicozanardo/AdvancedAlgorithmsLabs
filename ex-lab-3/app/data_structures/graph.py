from collections import defaultdict
import math

import sys
sys.path.append('../')


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Lista di adiacenza
        self.totalVertex = 0
        self.totalEdges = 0
        self.V = set()
        self.E = []

    def add_vertex(self, value: int):
        self.V.add(value)
        #self.graph[value] = [] --> :cry:

    # Assunzione: viene chiamato appena dopo gli addVertex
    def add_edge(self, u: int, v: int, w: int):
        self.E.append((u, v, w))
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))

    def remove_edge(self, u: int, v: int, w: int):
        self.E.remove((u, v, w))
        self.graph[u].remove((v, w))
        self.graph[v].remove((u, w))


    def fully_remove_node(self, v: int):
        # for (u,w) in self.graph[v]:
        #     self.E.remove((v,u,w))
        if (v in self.graph.keys()):
            self.graph.pop(v)
        if (v in self.V):
            self.V.remove(v)

    def weightBetween(self, firstNode, secondNode):
        minWeight = float('inf')

        for index in range(0, len(self.E)):
            if (self.E[index][0] == firstNode and self.E[index][1] == secondNode) or (self.E[index][1] == firstNode and self.E[index][0] == secondNode):
                minWeight = self.E[index][2]
                break
        return minWeight
