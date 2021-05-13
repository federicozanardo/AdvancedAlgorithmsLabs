from collections import defaultdict
import sys
sys.path.append('../')
from data_structures.tsp import TSP
from data_structures.heap import Heap, Node

class Prim:

    """
    Algoritmo MST di Prim con Heap

    Pseudocodice
    Prim(G,s)
        for each u in V do
            key[u] <- inf
            parents(u) <- null
        key[s] <- 0
        Q <- V
        while Q!=empty do
            u <- extractMin(Q)
            for each v adjacent to u do
                if v in Q and w(u,v) < key[v] then
                    parents(v) <- u
                    key[v] <- w(u,v)

    prim_mst(G: graph, s: node) : (defaultdict(list), defaultdict(list))
        G = grafo su cui eseguire l´algoritmo
        s = nodo di partenza per l´algoritmo
    Ritorna le mappe delle chiavi e dei parent
    """
    def prim_mst(self, T, s):

        """
        key: defaultdict(list) = mappa delle chiavi. Un valore è in forma key[nodo] = peso_nodo
        parent: defaultdict(list) = mappa dei parent. Un valore è in forma parent[nodo] = nodo_di_provenienza
        Q: Heap = heap contenente i nodi del MST risultante
        """
        key = defaultdict(list)
        parent = defaultdict(list)
        Q = Heap()

        """
        Inizializzazione
        * Per ogni nodo node di G\{s}, key[node] = Inf. key[s] = 0
        * Per ogni nodo node di G, parent[node] = nil
        * Q <- V
        """
        for i in range(len(T.nodes)+1):
            key[i] = 0 if s==i else float('inf')
            parent[i] = None
            Q.insert(Node(i, key[i]))
            
        print('dimensione di Q', len(Q.list))

        # for node in T.nodes:
        #     key[node] = 0 if s==node else float('inf')
        #     parent[node] = None
        #     Q.insert(Node(node, key[node]))
        
        """
        Calcolo della mappa delle chiavi e dei parent
        Finché l´heap Q non è vuoto
            estrai il nodo di peso minimo. u = (index,weight)
            Per ogni nodo v con peso w adiacente a u
                Se il nodo è presente in Q e il peso in Q è minore del peso di v
                    parent[v] = u
                    key[v] = w
                    aggiorna Q con il nuovo nodo di index v e peso key[v]
        """
        #print(len(T.adjMatrix[0]))
        while Q.currentSize != 0:
            u = (Q.extractMin()).toTuple()
            print('U=',u)
            for j in range(1, len(T.adjMatrix[int(u[0])])):
                if Q.search(j) and T.adjMatrix[int(u[0])][j] < key[j]:
                    parent[j] = u
                    key[j] = T.adjMatrix[int(u[0])][j]
                    print('J=',j)
                    Q.searchAndUpdateWeight(j, key[j])

            # for (v,w) in G.graph[u[0]]:
            #     if Q.search(v) and w < key[v]:
            #         parent[v] = u
            #         key[v] = w
            #         Q.searchAndUpdateWeight(v, key[v])
                    
        return key, parent

    """
    get_weight(key: defaultdict(list)) : int
        key = mappa di nodi del MST. Per ogni nodo node, key[node] = peso_nodo
    Ritorna la somma dei pesi del MST
    """
    def get_weight(self, key):
        sum = 0
        for (_, v) in key.items():
            if v!= float('inf'):
                sum += v
        return sum