from data_structures.disjoint_set import DisjointSet
from algorithms.merge_sort import MergeSort


class KruskalUnionFind:

    # Pseudo-codice Kruskal con Union-Find
    #
    # Complessità temporale: O(m * log(n))
    #
    # Kruskal-Union-Find(G, w)
    #   A = empty_set
    #   for each vertex belongs to G.V
    #     make-set(v)
    #   sort the edges of G.E into nondecreasing order by weight w
    #   for each edge (u, v) belongs to G.E, taken in nondecreasing order by weight
    #     if find-set(u) != find-set(v)
    #       A = A U {(u, v)}
    #       Union(u, v)
    #   return A
    def kruskal_union_find(self, G):
        ds = DisjointSet(len(G.V))

        # A è una lista che conterrà i lati che costituiscono il Minimum Spanning Tree
        A = []

        # Inserisco tutti i nodi nella struttura dati DisjointSet
        #
        # Complessità temporale: teta(n)
        for v in G.V:
            ds.make_set(int(v))

        # Ordina i lati in base al loro peso, in ordine crescente
        #
        # Complessità temporale: teta(m * log(m)))
        merge_sort = MergeSort()
        merge_sort.algorithm(G.E, 0, len(G.E) - 1)

        # Complessità temporale: O(m * log(n))
        for (u, v, w) in G.E:

            # Se il parent dei due nodi non è uguale, allora inserisco il lato che congiunge u e v di peso w
            if ds.find_set(int(u)) != ds.find_set(int(v)):
                A.append((u, v, w))
                ds.union_by_size(int(u), int(v))

        return A
