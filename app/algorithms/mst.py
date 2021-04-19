import copy
from collections import defaultdict
import sys

sys.path.append('../')

from data_structures.disjoint_set import DisjointSet
from data_structures.graph import Graph


class MST:
    DISCOVERY_EDGE = 0
    CROSS_EDGE = 1

    # Pseudo-code
    #
    # Kruskal-Naive(G)
    #     A = empty_set
    #     sort edges if G by cost
    #     for each edge e in nondecreasing order of cost
    #         if A U {e} is acyclic
    #             A = A U {e}
    #     return A

    def kruskal_naive(self, G):
        A = Graph()

        self._mergeSort(G.E, 0, len(G.E) - 1)

        for (u, v, w) in G.E:
            if self._is_acyclic(A, (u, v, w)):
                A.add_vertex(u)
                A.add_vertex(v)
                A.add_edge(u, v, w)

            # Ottimizzazione: mi fermo quando ho aggiunto n - 1 archi
            if len(G.V) == len(A.E) - 1:
                break

        return A

    def _is_acyclic(self, A: Graph, e):
        (u, v, w) = e
        # A_graph = copy.deepcopy(A)  # TODO: optimization 

        A.add_vertex(u)
        A.add_vertex(v)
        A.add_edge(u, v, w)

        # FIXME: before was: s = A_graph.V[0]
        firstVertex = A.V.pop()
        s = firstVertex
        A.V.add(firstVertex)
        flag = self._check_cross_edge(self.BFS(A, s))

        # TODO: remove edge
        A.E.remove((u, v, w))
        indexU = 0
        for x in A.graph[u]:
            if x != (v, w):
                indexU += 1
            else:
                break

        indexV = 0
        for x in A.graph[v]:
            if x != (u, w):
                indexV += 1
            else:
                break

        A.graph[u].pop(indexU)
        A.graph[v].pop(indexV)

        return not flag

    def BFS(self, G: Graph, s):
        # Create a queue
        Q = []

        vertices_visited = defaultdict(bool)
        for v in G.V:
            vertices_visited[v] = False

        # None = not visited
        # 0 = discovery edge
        # 1 = cross edge
        edges_visited = defaultdict()

        for (u, v, w) in G.E:
            edges_visited[(u, v)] = None

        Q.append(s)

        vertices_visited[s] = True

        while Q != []:
            v = Q.pop(0)

            for (u, w) in G.graph[v]:
                if (u, v) in edges_visited:
                    e = (u, v)
                else:
                    e = (v, u)

                if edges_visited[e] is None:
                    if not vertices_visited[u]:
                        edges_visited[e] = self.DISCOVERY_EDGE
                        vertices_visited[u] = True
                        Q.append(u)
                    else:
                        edges_visited[e] = self.CROSS_EDGE

        return edges_visited

    def _check_cross_edge(self, edges_visited):
        for w in edges_visited:
            if edges_visited[w] == 1:
                return True
        return False

    # Pseudo-code
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
        A = []

        for v in G.V:
            ds.make_set(int(v))

        # Ordina i lati con merge sort (complessità: O(nlogn))
        self._mergeSort(G.E, 0, len(G.E) - 1)

        for (u, v, w) in G.E:
            if ds.find_set(int(u)) != ds.find_set(int(v)):
                A.append((u, v, w))
                ds.union_by_size(int(u), int(v))

        return A

    def _mergeSort(self, array, left, right):
        if left < right:
            m = (left + (right - 1)) // 2

            self._mergeSort(array, left, m)
            self._mergeSort(array, m + 1, right)
            self._merge(array, left, m, right)

    def _merge(self, arr, left, m, right):
        n1 = m - left + 1
        n2 = right - m

        L = [0] * n1
        R = [0] * n2

        for i in range(0, n1):
            L[i] = arr[left + i]

        for j in range(0, n2):
            R[j] = arr[m + 1 + j]

        i = 0
        j = 0
        k = left

        while i < n1 and j < n2:
            (_, _, w1) = L[i]
            (_, _, w2) = R[j]

            if int(w1) <= int(w2):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1

            k += 1

        # Copy the remaining elements of L[], if there are any
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        # Copy the remaining elements of R[], if there are any
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
