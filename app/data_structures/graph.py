from collections import defaultdict

import sys
sys.path.append('../')


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list
        self.V = set()
        self.E = []

    def add_vertex(self, value):
        self.V.add(value)
        self.graph[value] = []

    # assunzione: viene chiamato appena dopo gli addVertex
    def add_edge(self, u, v, w):
        self.E.append((u, v, w))
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))
