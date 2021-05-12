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
        print(self.tsp.etype)
        for i in range(1, self.tsp.dimension+1):
            S.append(i)
            self.d[i] = {"w": None, "path": []}
            self.p[i].append(None)
        return self.hk_visit(1, S)

    # PRE: S sottoinsieme di V, v € S
    # POST: d[v,S] è il peso / distanza del cammino minimo da 0 a v che visita tutti i vertici in S, p[v,S] è il predecessore di v
    # S = vertici da scorrere presenti in V
    # v = vertice corrente
    def hk_visit(self, v, S):
        # print("Visiting: ", v, "Remaining: ", len(S))
        
        # Caso base 1: soluzione è il peso dell'arco {v, 1}
        if len(S) == 1 and v == S[0]:
            return self.tsp.adjMatrix[v][1]

        # Caso base 2: se il peso è già stato calcolato ritorno il peso
        elif self.d[v]['w'] != None: 
            return self.d[v]['w']

        # Caso ricorsivo: cerco il cammino minimo tra tutti i sottocammini 
        else:
            mindist = float('inf')
            minprec = None

            # Ottengo SS = S \ {v}
            SS = copy.deepcopy(S)
            SS.remove(v)

            for u in SS:
                
                # Calcolo ricorsivamente il peso della distanza nei sottocammini
                dist = self.hk_visit(u, SS)

                # Recupero il peso dell'arco {u, v}
                w = self.tsp.adjMatrix[u][v]

                # Prendo il minimo della distanza tra quello precedente e quello nuovo
                if (dist + w) < mindist:
                    mindist = dist + w
                    minprec = u
                    self.d[v]['path'].append(u)
            
            # Assegno il nuovo peso calcolato che risulta il cammino minimo
            self.d[v]['w'] = mindist
            self.p[v] = minprec
            return mindist
