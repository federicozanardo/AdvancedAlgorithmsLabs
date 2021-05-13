import sys
import math
from collections import defaultdict
sys.path.append('../')
import numpy

# PRE = in nodes le coordinate sono in radianti
class TSP:
    def __init__(self):
        self.name = ''
        self.dimension = 0
        self.etype = ''
        self.nodes = defaultdict(list)
        self.adjMatrix = []


    def add_node(self, i: int, x: float, y: float):
        if(self.etype == 'GEO'):
            degX, degY = int(x), int(y)
            minX, minY = x - degX, y - degY
            x, y = math.pi*(degX+5.0*minX/3.0)/180.0, math.pi*(degY+5.0*minY/3.0)/180.0
        self.nodes[i] = [x,y]

    # FUNZIONA (tm) ?
    # def get_weight(self, first: int, sec: int):
    #     RRR = 6378.388
    #     q1 = math.cos(self.nodes[first][1] - self.nodes[sec][1])
    #     q2 = math.cos(self.nodes[first][0] - self.nodes[sec][0])
    #     q3 = math.cos(self.nodes[first][0] + self.nodes[sec][0])
    #     final = (RRR*math.acos((0.5*((1.0+q1)*q2 - (1.0-q1)*q3))) + 1.0)
    #     if self.etype == 'GEO':
    #         return math.floor(final)
    #     else:
    #         return int(round(final))

    def get_weight(self, first: int, sec: int):
        if self.etype == 'GEO':
            RRR = 6378.388
            q1 = math.cos(self.nodes[first][1] - self.nodes[sec][1])
            q2 = math.cos(self.nodes[first][0] - self.nodes[sec][0])
            q3 = math.cos(self.nodes[first][0] + self.nodes[sec][0])
            return int(RRR * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0)
        else:
            return math.floor(math.sqrt((self.nodes[sec][1]-self.nodes[first][1])**2 + (self.nodes[sec][0]-self.nodes[first][0])**2))

    def calculateAdjMatrix(self):
        for i in range(self.dimension+1):
            self.adjMatrix.append([0 for i in range(self.dimension+1)])

        for i in range(1, self.dimension+1):
            for j in range(1, self.dimension+1):
                if i == j:
                    self.adjMatrix[i][j] = 0
                else:
                    self.adjMatrix[i][j] = self.adjMatrix[j][i] = self.get_weight(i, j)

        #self.printAdjMatrix()

    def printAdjMatrix(self):
        print('\n')
        print('\n'.join([''.join(['{:4}'.format((item)) for item in row]) 
      for row in self.adjMatrix]))

    # funziona
    def delete_node(self, index: int):
        if index in self.nodes.keys():
            self.nodes.pop(index)
            for i in range(1, self.dimension+1):
                self.adjMatrix[i][index] = self.adjMatrix[index][i] = 0
            self.dimension = self.dimension - 1


    def get_min_node(self, visited, index: int):
        minWeight = float('inf')
        minIndex = -1
        for i in range(1, self.dimension+1):
            if self.adjMatrix[i][index] < minWeight and self.adjMatrix[i][index] != 0 and i not in visited:
                minIndex = i
                minWeight = self.adjMatrix[index][i]
        
        return([minIndex, self.nodes[minIndex][0], self.nodes[minIndex][1]])
