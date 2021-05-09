from collections import defaultdict
import sys
sys.path.append('../')
from data_structures.graph import Graph
from data_structures.heap import Heap, Node


# TODO: must test, not tried yet
class HeldKarp:

    def __init__(self):
        self.d = defaultdict(list)
        self.p = defaultdict(list)

    # graph = struttura dati del grafo
    def hk_init(self, graph):
        # TODO: deep copy time? 
        return self.hk_visit(0, graph.graph)

    # PRE: S sottoinsieme di V, v € S
    # POST: d[v,S] è il peso / distanza del cammino minimo da 0 a v che visita tutti i vertici in S, p[v,S] è il predecessore di v
    # S = vertici da scorrere presenti in V
    # v = vertice corrente
    def hk_visit(self, v, S):
        if len(S) == 1 and v in S: # S[v] != null
            (_,w) = S[v]
            return w
        elif v in self.d: # d[v] != null
            return self.d[v]
        else:
            mindist = float('inf')
            minprec = None
        
        # FIXME: many doubts about the legality of this move
            (u, w) = S[v]
            S[v].remove((u, w))
            for (u, w) in S:
                dist = self.hk_visit(u, S)
                if dist + w < mindist:
                    mindist = dist + w
                    minprec = u
            self.d[v] = mindist
            self.p[v] = minprec
            return mindist
