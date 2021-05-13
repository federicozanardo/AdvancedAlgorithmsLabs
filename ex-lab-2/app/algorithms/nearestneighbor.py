from typing import final
from data_structures.tsp import TSP
import copy as cp

class NearestNeighbor:
    def algorithm(self, graph: TSP):
        
        startingGraph = cp.deepcopy(graph)
        finalPath = []
        visited = []
        startingNode = startingGraph.nodes[1]
        finalPath.append([1, startingNode[0], startingNode[1]])
        startingGraph.delete_node(1)
        visited.append(1)
        
        totalWeight = 0

        # sia (v1,...,vk) il cammino corrente: prendi il vertice vk+1 non presente e con distanza minima da vk
        # inserisci vk+1 dopo vk
        # ripeti finché tutti i vertici non sono nel cammino
        while startingGraph.dimension != 0:
            lastEl = finalPath[-1][0]
            visited.append(lastEl)
            minimumNode = graph.get_min_node(visited, lastEl)
            finalPath.append([minimumNode[0], minimumNode[1], minimumNode[2]])

            totalWeight += graph.adjMatrix[lastEl][finalPath[-1][0]]
            #totalWeight += graph.get_weight(lastEl, finalPath[-1][0])
            startingGraph.delete_node(minimumNode[0])
        
        # aggiungi il vertice iniziale alla fine del cammino
        totalWeight += graph.adjMatrix[finalPath[-1][0]][1]
        finalPath.append([1, startingNode[0], startingNode[1]])

        return totalWeight
        