import sys
import math
from collections import defaultdict
sys.path.append('../')

"""
Classe TSP
tsp: TSP = (name: string, dimension: int, etype: string, nodes: defaultdict(list), adjMatrix: list[])
    name = nome del dataset
    dimension = dimensione del dataset
    etype = tipo del dataset (GEO|EUC_2D)
    nodes = lista dei nodi del grafo
    adjMatrix = matrice di adiacenza dei nodi del grafo
"""
class TSP:

    def __init__(self):
        self.name = ''
        self.dimension = 0
        self.etype = ''
        self.nodes = defaultdict(list)
        self.adjMatrix = []


    """
    add_node(i: int, x: float, y: float): void
        i = indice del nodo
        x = latitudine
        y = longitudine
    Aggiunge un nodo alla lista dei nodi; non modifica la matrice di adiacenza.
    Se il dataset è in formato GEO, converte x e y in radianti.
    """
    def add_node(self, i: int, x: float, y: float):
        if(self.etype == 'GEO'):
            degX, degY = int(x), int(y)
            minX, minY = x - degX, y - degY
            x, y = math.pi*(degX+5.0*minX/3.0)/180.0, math.pi*(degY+5.0*minY/3.0)/180.0
        self.nodes[i] = [x,y]

    """
    get_weight(first: int, sec: int): float
        first = indice del primo nodo
        second = indice del secondo nodo
    Ritorna il peso tra un nodo e l'altro.
    Distingue se le coordinate sono lat,long o euclidee
    """
    def get_weight(self, first: int, sec: int):
        if self.etype == 'GEO':
            RRR = 6378.388
            q1 = math.cos(self.nodes[first][1] - self.nodes[sec][1])
            q2 = math.cos(self.nodes[first][0] - self.nodes[sec][0])
            q3 = math.cos(self.nodes[first][0] + self.nodes[sec][0])
            return int(RRR * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0)
        else:
            return math.sqrt((self.nodes[sec][1]-self.nodes[first][1])**2 + (self.nodes[sec][0]-self.nodes[first][0])**2)

    """
    calculateAdjMatrix(): void
    Calcola la matrice di adiacenza (matrice simmetrica sulla diagonale).
    Assumiamo che venga chiamata dopo aver inserito i nodi per la prima volta nel TSP.
    """
    def calculateAdjMatrix(self):
        for i in range(self.dimension+1):
            self.adjMatrix.append([0 for i in range(self.dimension+1)])

        for i in range(1, self.dimension+1):
            for j in range(1, self.dimension+1):
                if i == j:
                    self.adjMatrix[i][j] = 0
                else:
                    self.adjMatrix[i][j] = self.adjMatrix[j][i] = self.get_weight(i, j)

    """
    printAdjMatrix(): void
    Funzione di utilità per la stampa della matrice di adiacenza.
    """
    def printAdjMatrix(self):
        print('\n')
        print('\n'.join([''.join(['{:4}'.format((item)) for item in row]) 
      for row in self.adjMatrix]))

    """
    delete_node(index: ind): void
        index = indice del nodo da eliminare
    Elimina, se esiste, un nodo dalla lista dei nodi. Aggiorna inoltre la matrice di adiacenza.
    """
    def delete_node(self, index: int):
        if index in self.nodes.keys():
            self.nodes.pop(index)
            for i in range(1, self.dimension+1):
                self.adjMatrix[i][index] = self.adjMatrix[index][i] = 0
            self.dimension = self.dimension - 1

    """
    get_min_node(visited: list, index: ind): [int, float, float]
        visited = lista di nodi visitati in cui NON ricercare il minimo
        index = indice del nodo di cui trovare il vicino di peso minimo
    Ritorna il nodo di peso minimo da index che non sia ancora stato visitato dall'algoritmo Nearest Neighbor
    """
    def get_min_node(self, visited, index: int):
        minWeight = float('inf')
        minIndex = -1
        for i in range(1, self.dimension+1):
            if self.adjMatrix[i][index] < minWeight and self.adjMatrix[i][index] != 0 and i not in visited:
                minIndex = i
                minWeight = self.adjMatrix[index][i]
        
        return([minIndex, self.nodes[minIndex][0], self.nodes[minIndex][1]])
