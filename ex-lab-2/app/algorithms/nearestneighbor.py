from typing import final
from data_structures.tsp import TSP
import copy as cp

class NearestNeighbor:
    def algorithm(self, graph: TSP):
        
        """
        startingGraph: TSP = grafo da cui vengono estratti man mano i nodi
        finalPath: list = lista contenente il percorso man mano trovato
        visited: list = visita dei nodi visitati
        totalWeight: float = peso totale del grafo tsp
        """
        startingGraph = cp.deepcopy(graph)
        finalPath, visited = [], []
        totalWeight = 0

        """Inizializzazione
        * Prendo il primo nodo
            * Lo aggiungo a finalPath
            * Aggiungo il suo indice a visited
        * Elimino il nodo dall'insieme di partenza
        """
        startingNode = startingGraph.nodes[1]
        finalPath.append([1, startingNode[0], startingNode[1]])
        visited.append(1)

        startingGraph.delete_node(1)
        
        """
        Ricerca dei nodi
        * Sia (V1,...,Vk) il cammino corrente:
            * Prendo il vertice Vk+1 non presente e con distanza minima da Vk
            * Inserisco Vk+1 dopo Vk
            * Aggiorno il valore del peso
            * Elimino il nodo Vk+1 dall'insieme di partenza
        """
        while startingGraph.dimension != 0:
            lastEl = finalPath[-1][0]
            visited.append(lastEl)
            minimumNode = graph.get_min_node(visited, lastEl)
            finalPath.append([minimumNode[0], minimumNode[1], minimumNode[2]])

            totalWeight += graph.adjMatrix[lastEl][finalPath[-1][0]]
            startingGraph.delete_node(minimumNode[0])
        
        # Aggiungo il nodo iniziale per chiudere il grafico
        totalWeight += graph.adjMatrix[finalPath[-1][0]][1]
        finalPath.append([1, startingNode[0], startingNode[1]])

        return totalWeight
        