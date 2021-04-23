from collections import defaultdict
import sys
sys.path.append('../')

from data_structures.disjoint_set import DisjointSet
from data_structures.graph import Graph
from data_structures.heap import Heap, Node

class Prim:

    # Pseudocode
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
        key = defaultdict(list)
        parent = defaultdict(list)

        Q = Heap()


        for node in G.V:
            key[node] = 0 if s==node else float('inf')
            parent[node] = None
            Q.insert(Node(node, key[node]))

        while Q.currentSize != 0:
            u = (Q.extractMin()).toTuple()

            for (v,w) in G.graph[u[0]]:
                if Q.search(v) and w < key[v]:
                    parent[v] = u
                    key[v] = w 
                    Q.searchAndUpdateWeight(v, key[v])
                    
        return key, parent

    def get_weight(self, key):
        sum = 0
        for (k, v) in key.items():
            if v!= float('inf'):
                sum += v
        return sum