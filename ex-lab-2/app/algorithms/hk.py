from collections import defaultdict
import copy
import sys
sys.path.append('../')
from data_structures.graph import Graph
from data_structures.tsp import TSP
from data_structures.heap import Heap, Node



class HeldKarp:

    def __init__(self):
        self.d = defaultdict(list)
        self.p = defaultdict(list)
        self.tsp = None

    def _keygen(self, v, S):
        o = str(v) + ",["
        for i in S:
            o = o + str(i) + " "
        o = o + "]"
        return o

    # graph = struttura dati del grafo
    def hk_init(self, tsp):
        self.tsp = copy.deepcopy(tsp)
        S = []
        #print(self.tsp.etype)
        for i in range(1, self.tsp.dimension+1):
            S.append(i)
            #self.d[i] = {"w": None}
            self.p[i].append(None)
        # print(S)
        return self.hk_visit(1, S)# eh no, manca 1, no ok è giusto PERCHÉ PYTHON GIUSTO
        
        # OK FORSE HO CAPITO: NON STA COPIANDO BENE LA LISTA PERCHÉ STA COSA NON È NORMALE
        # DOVREBBE ANDARE IN RICORSIONE E INVECE TOGLIE TUTTO E POI RIMANE VUOTA
        # kk e se fosse così sarebbe bene o male? Nel senso, è un problema "del cazzo" o bisogna ripensare tutto?
        # VUOL DIRE CHE DEEPCOPY È FOTTUTAMENTE ROTTO
        # Non mi stupisce
         
        
    # PRE: S sottoinsieme di V, v € S
    # POST: d[v,S] è il peso / distanza del cammino minimo da 0 a v che visita tutti i vertici in S, p[v,S] è il predecessore di v
    # S = vertici da scorrere presenti in V
    # v = vertice corrente
    def hk_visit(self, v, S):
        # print("Visiting: ", v, "Remaining: ", len(S))
        print(self._keygen(v, S))
        
        # Caso base 1: soluzione è il peso dell'arco {v, 1}
        if len(S) == 1 and v == S[0]:
            #print("i came: ", self.tsp.adjMatrix[v][1])
            return self.tsp.adjMatrix[v][1]

        # Caso base 2: se il peso è già stato calcolato ritorno il peso
        elif self._keygen(v, S) in self.d.keys():
            return self.d[self._keygen(v, S)]

        # Caso ricorsivo: cerco il cammino minimo tra tutti i sottocammini 
        else:
            mindist = float('inf')
            minprec = None
            # Ottengo SS = S \ {v}
            #SS = copy.deepcopy(S)
            #SS.remove(v)
            
            SE = []

            for x in S:
                if x != v:
                    SE.append(x)

            # print(SE)
            
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
            self.d[self._keygen(v, S)] = mindist 
            self.p[v] = minprec
            return mindist
