import sys


sys.path.append('../')

from data_structures.graph import Graph


class MST:

    # def kruskal_naive(self, G: Graph):
    #     algorithm = KruskalNaive()
    #     return algorithm.kruskal_naive(G)

    # def kruskal_union_find(self, G: Graph):
    #     algorithm = KruskalUnionFind()
    #     return algorithm.kruskal_union_find(G)

    
    def get_mst_weight(self, E):
        summation = 0

        for (u, v, w) in E:
            summation += int(w)

        return summation
