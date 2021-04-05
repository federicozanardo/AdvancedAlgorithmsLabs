from collections import defaultdict
import sys
sys.path.append('../')


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list
        self.V = []
        self.E = []

    def add_vertex(self, value):
        if value not in self.V:
            self.V.append(value)
            self.graph[value] = []

    def add_edge(self, u, v, w):
        if u in self.V and v in self.V:
            if (u, v, w) not in self.E and (v, u, w) not in self.E:
                self.E.append((u, v, w))
                self.graph[u].append((v, w))
                self.graph[v].append((u, w))
