from collections import defaultdict
import sys
sys.path.append('../')

from data_structures.disjoint_set import DisjointSet
from data_structures.graph import Graph
from data_structures.heap import Heap, Node

class Prim:
    # Prim(G,s)
    #     for each u in V do
    #         key[u] <- inf
    #         parents(u) <- null
    #     key[s] <- 0
    #     Q <- V

    #     while Q!=empty do
    #         u <- extractMin(Q)
    #         for each v adjacent to u do
    #             if v in Q and w(u,v) < key[v] then
    #                 parents(v) <- u
    #                 key[v] <- w(u,v)

    def prim_mst(self, G, s):
        # Initialization & Q <- V
        key = {}
        parent = {} #defaultdict(list)

        Q = Heap()

        for node in G.V:
            key[int(node)] = 0 if s==int(node) else float('inf')
            #key.insert(int(node), 0 if s==node else float('inf'))
            parent[int(node)] = None
            #parent.insert(int(node), None)
            Q.insert(Node(int(node), key[int(node)]))

        # algoritmo
        while Q.currentSize != 0:
            u = (Q.extractMin()).toTuple()
            for (v,w) in G.graph[str(u[0])]:
                if Q.search(v) and float(w) < key[int(v)]:
                    parent[int(v)] = u
                    key[int(v)] = float(w)
        