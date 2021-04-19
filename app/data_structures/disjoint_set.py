import sys
sys.path.append('../')

class DisjointSet:
    def __init__(self, n):
        self.nodes = [DisjointSetNode] * n

    def make_set(self, value: int):
        x = DisjointSetNode()
        x.value = value
        x.parent = x
        x.size = 1
        self.nodes[value - 1] = x

    def find_set(self, x: int):
        if self.nodes[x - 1].parent != self.nodes[x - 1]:
            self.nodes[x - 1].parent = self.find_set(self.nodes[x - 1].parent.value)
            return self.nodes[x - 1].parent
        else:
            return self.nodes[x - 1]

    def union_by_size(self, x: int, y: int):
        x = self.find_set(x)
        y = self.find_set(y)

        if x != y:
            if x.size < y.size:
                (x, y) = (y, x)

            y.parent = x
            x.size += y.size


class DisjointSetNode:
    value = None
    parent = None
    size = None
