from collections import defaultdict
import copy
import sys
sys.path.append('../')
from data_structures.graph import Graph
from data_structures.tsp import TSP
from data_structures.heap import Heap, Node


# TODO: must test, not tried yet
class HeldKarp:

    def __init__(self):
        self.d = defaultdict(list)
        self.p = defaultdict(list)
        self.tsp = None

    # graph = struttura dati del grafo
    def hk_init(self, tsp):
        self.tsp = copy.deepcopy(tsp)
        S = []
        for i in range(1, self.tsp.dimension+1):
            S.append(i)
            self.d[i].append(None)
            self.p[i].append(None)
        return self.hk_visit(1, S)

    # PRE: S sottoinsieme di V, v € S
    # POST: d[v,S] è il peso / distanza del cammino minimo da 0 a v che visita tutti i vertici in S, p[v,S] è il predecessore di v
    # S = vertici da scorrere presenti in V
    # v = vertice corrente
    def hk_visit(self, v, S):
        print("Visiting: ", v, "Remaining: ", len(S))
        if len(S) == 1 and v in S: # S[v] != null
            return self.tsp.get_weight(v, 1)
        elif v in self.d and self.d[v][0] != None: # d[v] != null
            return self.d[v][0]
        else:
            mindist = float('inf')
            minprec = None
        
            # FIXME: many doubts about the legality of this move
            S.remove(v)
            for u in S:
                dist = self.hk_visit(u, S)
                w = self.tsp.get_weight(u, v)
                if dist + w < mindist:
                    mindist = dist + w
                    minprec = u
            self.d[v][0] = mindist
            self.p[v][0] = minprec
            return mindist
