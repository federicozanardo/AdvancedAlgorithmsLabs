import sys
import math
from collections import defaultdict
sys.path.append('../')

# PRE = in nodes le coordinate sono in radianti
class TSP:
    def __init__(self):
        self.name = ''
        self.dimension = 0
        self.etype = 'EUC_2D'
        self.nodes = defaultdict(list)
        self.adjMatrix = []

    def add_node(self, i: int, x: float, y: float):
        if(self.etype == 'GEO'):
            degX, degY = int(x), int(y)
            minX, minY = x - degX, y - degY
            x, y = math.pi*(degX+5*minX/3)/180.0, math.pi*(degY+5*minY/3)/180.0
        self.nodes[i] = [x,y]

    def get_weight(self, first: int, sec: int):
        RRR = 6378.388
        q1 = math.cos(self.nodes[first][1] - self.nodes[sec][1])
        q2 = math.cos(self.nodes[first][0] - self.nodes[sec][0])
        q3 = math.cos(self.nodes[first][0] + self.nodes[sec][0])
        final = RRR*math.acos(0.5*((1.0+q1)*q2 - (1.0-q1)*q3)) + 1.0
        if self.etype == 'GEO':
            return math.floor(final)
        else:
            return int(round(final))
        
    def calculateAdjMatrix(self):
        for i in range(1, self.dimension+1):
            self.adjMatrix.append([0 for i in range(1, self.dimension+1)])

        for i in range(1, self.dimension):
            for j in range(1, self.dimension):
                self.adjMatrix[i][j] = self.get_weight(i, j)
                self.adjMatrix[j][i] = self.adjMatrix[i][j]