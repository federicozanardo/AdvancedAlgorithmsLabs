import math
import sys
sys.path.append('../')


class DisjointSet:
    def __init__(self):
        self.parents = [math.inf]
        self.sizes = [0]

    def make_set(self, x: int):
        self.parents.append(x)
        self.sizes.append(1)

    def find_set(self, x: int):
        root = x

        while self.parents[root] != root:
            root = self.parents[root]

        return root

    def union_by_size(self, x: int, y: int):
        i = self.find_set(x)
        j = self.find_set(y)

        if i != j:
            if self.sizes[i] >= self.sizes[j]:
                self.parents[j] = i
                self.sizes[i] += self.sizes[j]
            else:
                self.parents[i] = j
                self.sizes[j] += self.sizes[i]
