from collections import defaultdict
import sys
sys.path.append('../')


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)  # Adjacency list
        self.V = []
        self.E = []

    def add_vertex(self, value):
        ok = True
        if value in self.V:
            ok = False

        if ok:
            self.V.append(value)
            self.graph[value] = []

    def add_edge(self, u, v, w):
        ok = True
        for i in range(len(self.E)):
            if (u, v, w) == self.E[i] or (v, u, w) == self.E[i]:
                ok = False

        if ok:
            self.E.append((u, v, w))
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))
