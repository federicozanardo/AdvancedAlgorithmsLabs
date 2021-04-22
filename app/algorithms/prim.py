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
        key = defaultdict(list)
        parent = defaultdict(list)

        Q = Heap()

        for node in G.V:
            key[node] = 0 if s==node else float('inf')
            #key.insert(int(node), 0 if s==node else float('inf'))
            parent[node] = None
            #parent.insert(int(node), None)
            Q.insert(Node(node, key[node]))

        Q.print()
        # algoritmo che non sta funzionando
        while Q.currentSize != 0:
            Q.print()
            u = (Q.extractMin()).toTuple()
            for (v,w) in G.graph[u[0]]:
                print(v)
                #print(Q.search(v))
                if Q.search(v) and w < key[v]:
                    print(v)
                    parent[v] = u
                    key[v] = w
                    Q.searchAndUpdateWeight(v, w)
                
            print(G.graph[u[0]])
            print(key)
        for (x, y) in G.graph[u[0]]:
            print(x)
        return key

    def get_weight(self, key):
        sum = 0
        for (k, v) in key.items():
            #print(v)
            if v!= float('inf'):
                sum += v
        return sum
        