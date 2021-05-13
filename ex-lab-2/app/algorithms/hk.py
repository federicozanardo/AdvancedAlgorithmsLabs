from collections import defaultdict
import sys
sys.path.append('../')
from data_structures.tsp import TSP



class HeldKarp:

    def __init__(self):
        self.d = defaultdict(list)
        self.p = defaultdict(list)
        self.tsp = None

    def _keygen(self, v, S):
        o = str(v) + ",[ "
        for x in S:
            o = o + str(x) + " "
        o = o + "]"
        return o

    def hk_init(self, tsp):
        self.tsp = tsp
        S = []
        for i in range(1, self.tsp.dimension+1):
            S.append(i)
        return self.hk_visit(1, S)
        
    # PRE: S sottoinsieme di V, v € S
    # POST: d[v,S] è il peso / distanza del cammino minimo da 0 che visita tutti i vertici in S, 
    #       p[v,S] è il predecessore di v
    # S = vertici da scorrere presenti in V
    # v = vertice corrente
    def hk_visit(self, v, S):
        
        currentKey = self._keygen(v, S)
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
            
            # Ricavo insieme SS = S \ {v}
            # ndr: più veloce rispetto a una deepcopy, complessità O(n-1)
            SE = []
            for x in S:
                if x != v:
                    SE.append(x)
            
            for u in SE:
                
                # Calcolo ricorsivamente il peso della distanza nei sottocammini
                dist = self.hk_visit(u, SE)

                # Recupero il peso dell'arco {u, v}
                w = self.tsp.adjMatrix[u][v]

                # Prendo il minimo della distanza tra quello precedente e quello nuovo
                if (dist + w) < mindist:
                    mindist = dist + w
                    minprec = u
         
            # Assegno il nuovo peso calcolato che risulta il cammino minimo
            self.d[currentKey] = mindist 
            self.p[currentKey] = minprec
            return mindist
