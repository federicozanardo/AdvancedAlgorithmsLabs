from collections import defaultdict
import sys
import time
sys.path.append('../')
from data_structures.tsp import TSP
sys.setrecursionlimit(5000)


class HeldKarp:

    # Costruttore di classe
    def __init__(self):
        self.d = defaultdict(list)
        self.p = defaultdict(list)
        self.tsp = None
        self.timeStart = None
        self.timeEnd = None


    # Inizializzazione e ritorno dei risultati di Held and Karp
    def hk_init(self, tsp):
        self.tsp = tsp
        S = []
        # Popolamento iniziale di S a partire dai nodi V
        for i in range(1, self.tsp.dimension+1):
            S.append(i)
        self.timeStart = time.perf_counter()
        result = self.hk_visit(1, S)
        self.timeEnd = time.perf_counter() - self.timeStart
        return result
        
    # PRE: S sottoinsieme di V, v € S
    # POST: d[v,S] è il peso / distanza del cammino minimo da 0 che visita tutti i vertici in S, 
    #       p[v,S] è il predecessore di v
    # S = vertici da scorrere presenti in V
    # v = vertice corrente
    def hk_visit(self, v, S):
        
        currentKey = str(v) + str(S)
        # print(currentKey)
        
        # Caso base 1: soluzione è il peso dell'arco {v, 1}
        if len(S) == 1 and v == S[0]:
            return self.tsp.adjMatrix[v][1]

        # Caso base 2: se il peso è già stato calcolato ritorno il peso
        elif currentKey in self.d.keys():
                return self.d[currentKey]

        # Caso ricorsivo: cerco il cammino minimo tra tutti i sottocammini 
        else:
            mindist = float('inf')
            minprec = None
            
            # Ricavo insieme SE = S \ {v}
            # ndr: più veloce rispetto a una deepcopy, complessità O(n-1)
            SE = []
            for x in S:
                if x != v:
                    SE.append(x)
            
            for u in SE:
                if time.perf_counter() - self.timeStart < 180.0:
                    # Calcolo ricorsivamente il peso della distanza nei sottocammini
                    dist = self.hk_visit(u, SE)

                    # Recupero il peso dell'arco {u, v}
                    w = self.tsp.adjMatrix[u][v]

                    # Prendo il minimo della distanza tra quello precedente e quello nuovo
                    if (dist + w) < mindist:
                        mindist = dist + w
                        minprec = u
                else:
                    return mindist

            # Assegno il nuovo peso calcolato che risulta il cammino minimo
            self.d[currentKey] = mindist
            self.p[currentKey] = minprec
            return mindist

# burma14.tsp 3323
# ulysses16.tsp 6859
# ulysses22.tsp 7188
# eil51.tsp 1050
# berlin52.tsp 17917
# kroD100.tsp 148525
# kroA100.tsp 167464
